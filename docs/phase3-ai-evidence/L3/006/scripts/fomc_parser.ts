import fs from 'node:fs';
import path from 'node:path';
import { GoogleGenAI, ThinkingLevel } from '@google/genai';
import { BASELINE_SCHEMA, DEFINITIONS, JURY_SCHEMA, PERSONAS, RULE_VERSION, scoreBaseline, validateShape } from './scoring';

export const MODEL = 'gemini-3.5-flash-lite';
const usage = 'npm run ai:score -- --statement ../data/statements/statement4.md --previous ../data/statements/previous4.md --output ../data/results/manual-statement4.json [--parallel]';
type Request = { systemInstruction: string; contents: string; temperature: number; responseJsonSchema: typeof BASELINE_SCHEMA };
type Reply = { text: string; modelVersion?: string; usage?: unknown };
type Invoke = (request: Request) => Promise<Reply>;

function read(file: string): string {
  const text = fs.readFileSync(file, 'utf8');
  if (!text.trim()) throw new Error(`Empty file: ${file}`);
  return text;
}

export function buildRequests(current: string, prior: string | null): Request[] {
  const contents = JSON.stringify({ CURRENT_STATEMENT: current, PRIOR_STATEMENT: prior });
  const baseline = read(path.join(__dirname, 'PASS1-BASELINE-PROMPT.md'))
    .replace('{{RULE_CATALOG}}', JSON.stringify(DEFINITIONS, null, 2));
  const jury = read(path.join(__dirname, 'PASS2-JURY-PROMPT.md'));
  return [
    { systemInstruction: baseline, contents, temperature: 0, responseJsonSchema: BASELINE_SCHEMA },
    ...PERSONAS.map(persona => ({ systemInstruction: jury.replace('{{PERSONA_ID}}', persona), contents, temperature: .2, responseJsonSchema: JURY_SCHEMA })),
  ];
}

// Separate calls: no chat history or baseline output is ever sent to the jury.
export async function runStudy(current: string, prior: string | null, invoke: Invoke, save: (record: any) => void = () => {}, parallel = false) {
  const requests = buildRequests(current, prior);
  const record: any = {
    run_status: 'in_progress', started_at: new Date().toISOString(),
    rule_version: RULE_VERSION, prompt_version: '0.5', model: MODEL, thinking: 'MEDIUM',
    jury_execution: parallel ? 'parallel' : 'sequential',
    calls: [], baseline: null, jury: {}, avg_jury_score: null, final_score: null, error: null,
  };
  save(record);
  try {
    const execute = async (i: number) => {
      const call: any = { pass: i === 0 ? 'baseline' : 'jury', persona: i === 0 ? null : PERSONAS[i - 1], request: requests[i] };
      record.calls.push(call);
      save(record);
      try {
        const reply = await invoke(requests[i]);
        call.response = reply;
        save(record); // Preserve raw responses even if JSON/schema validation fails.
        const parsed = JSON.parse(reply.text);
        if (i === 0) {
          record.baseline = scoreBaseline(parsed, current, prior);
          const { baseline_score, coverage, status, confidence } = record.baseline;
          record.phase4 = { baseline_score, coverage, status, confidence };
        } else {
          validateShape(parsed, JURY_SCHEMA);
          record.jury[PERSONAS[i - 1]] = parsed;
        }
        save(record);
      } catch (error) {
        call.error = error instanceof Error ? error.message : String(error);
        save(record);
        throw error;
      }
    };
    await execute(0);
    if (parallel) {
      // Await all outstanding calls so a failure cannot discard other responses.
      const outcomes = await Promise.allSettled([1, 2, 3].map(execute));
      const failed = outcomes.find(r => r.status === 'rejected');
      if (failed?.status === 'rejected') throw failed.reason;
    } else {
      for (let i = 1; i < requests.length; i++) await execute(i);
    }
    record.avg_jury_score = Number((PERSONAS.reduce((sum, persona) => sum + record.jury[persona].jury_score, 0) / PERSONAS.length).toFixed(1));
    record.final_score = record.baseline.baseline_score === null ? null
      : Number(((record.baseline.baseline_score + record.avg_jury_score) / 2).toFixed(1));
    record.run_status = 'completed';
    record.completed_at = new Date().toISOString();
    save(record);
    return record;
  } catch (error) {
    record.run_status = 'failed';
    record.error = error instanceof Error ? error.message : String(error);
    save(record);
    throw error;
  }
}

export function prepareOutput(output: string, inputs: string[]): void {
  if (fs.existsSync(output)) {
    const target = fs.statSync(output);
    for (const input of inputs) {
      const source = fs.statSync(input);
      if (target.dev === source.dev && target.ino === source.ino) {
        throw new Error('Output must not overwrite an input statement.');
      }
    }
  }
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, '{}\n', 'utf8');
}

async function main() {
  const argv = process.argv.slice(2);
  if (argv.includes('--help')) { console.log(usage); return; }
  const args: Record<string, string> = {};
  let parallel = false;
  for (let i = 0; i < argv.length; i++) {
    const key = argv[i];
    if (key === '--parallel' && !parallel) { parallel = true; continue; }
    if (!['--statement', '--previous', '--output'].includes(key) || !argv[i + 1] || argv[i + 1].startsWith('--') || args[key]) throw new Error(`Invalid arguments. Usage: ${usage}`);
    args[key] = argv[++i];
  }
  if (!args['--statement'] || !args['--output']) throw new Error(`Usage: ${usage}`);
  const current = read(path.resolve(args['--statement']));
  const prior = args['--previous'] ? read(path.resolve(args['--previous'])) : null;
  const output = path.resolve(args['--output']);
  const key = process.env.GEMINI_API_KEY?.trim() || read(path.join(__dirname, 'api_key')).trim();
  const client = new GoogleGenAI({ apiKey: key, httpOptions: { timeout: 90000 } });
  prepareOutput(output, [args['--statement'], args['--previous']].filter(Boolean).map(p => path.resolve(p)));
  let number = 0;
  const result = await runStudy(current, prior, async request => {
    console.log(`Call ${++number}/4: ${number === 1 ? 'baseline extraction' : PERSONAS[number - 2]}`);
    const response = await client.models.generateContent({
      model: MODEL, contents: request.contents,
      config: { systemInstruction: request.systemInstruction, temperature: request.temperature,
        responseMimeType: 'application/json', responseJsonSchema: request.responseJsonSchema,
        thinkingConfig: { thinkingLevel: ThinkingLevel.MEDIUM } },
    });
    return { text: response.text ?? '', modelVersion: response.modelVersion, usage: response.usageMetadata };
  }, record => fs.writeFileSync(output, `${JSON.stringify(record, null, 2)}\n`, 'utf8'), parallel);
  console.log(JSON.stringify({ ...result.phase4, avg_jury_score: result.avg_jury_score, final_score: result.final_score, jury: result.jury }, null, 2));
  console.log(`Saved full evidence and responses: ${output}`);
}

if (require.main === module) main().catch(error => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
