import React from 'react';

const DomainConfigPage = () => {
  return (
    <div className="p-8">
      <h2 className="text-2xl font-bold mb-6">Genome Editor</h2>
      <div className="grid grid-cols-3 gap-8">
        <div className="col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold mb-4">Edit Genome: uk_employment_tribunal</h3>
          <div className="font-mono text-sm bg-slate-50 p-4 rounded border border-slate-200 overflow-x-auto">
            <pre>{`extends: base_schema
domain:
  id: uk_employment_tribunal
  name: UK Employment Tribunal Analysis
jaiza:
  pattern_libraries: [discrimination_patterns, procedural_unfairness]
  alignment_frameworks: [legal]
muaina:
  output_templates: [tribunal_submission, copy_paste_emails, github_workflow]`}</pre>
          </div>
          <button className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700">
            Submit Evolution Proposal
          </button>
        </div>
        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h3 className="text-lg font-bold mb-4">Inheritance Map</h3>
          <div className="space-y-4">
            <div className="p-3 bg-indigo-50 border border-indigo-200 rounded text-center">Base Schema</div>
            <div className="text-center text-slate-400">↓</div>
            <div className="p-3 bg-green-50 border border-green-200 rounded text-center font-bold">UK Tribunal</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DomainConfigPage;
