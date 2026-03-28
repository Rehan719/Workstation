import React, { useState, useEffect } from 'react';
import { Card, Button, Badge } from '@workstation/ui';
import { Upload, FileText, CheckCircle2, Loader2, Database, Search, Trash2 } from 'lucide-react';
import axios from 'axios';

export const Ingest: React.FC = () => {
  const [files, setFiles] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchIngestedFiles();
  }, []);

  const fetchIngestedFiles = async () => {
    try {
      const resp = await axios.get('/api/v1/ingest/list');
      setFiles(resp.data);
    } catch (e) {
      console.error('Failed to fetch files', e);
    }
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.[0]) return;
    const file = e.target.files[0];

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('/api/v1/ingest/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      fetchIngestedFiles();
    } catch (e) {
      alert('Upload failed: ' + (e as any).message);
    } finally {
      setUploading(false);
    }
  };

  const filteredFiles = files.filter(f =>
    f.filename.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-12 pb-24">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-6xl font-black mb-1 text-white tracking-tighter uppercase italic">Content <span className="text-aura">Ingestion</span></h1>
          <p className="text-aura font-black uppercase text-[10px] tracking-[0.3em]">Knowledge Base Acquisition • Multi-Format Extraction • v1.0</p>
        </div>
        <div className="flex gap-4">
           <label className="cursor-pointer">
              <input type="file" className="hidden" onChange={handleFileUpload} disabled={uploading} />
              <Button className="bg-white text-sovereign shadow-xl pointer-events-none">
                 {uploading ? <Loader2 className="animate-spin mr-2" size={18} /> : <Upload className="mr-2" size={18} />}
                 {uploading ? 'Processing...' : 'Ingest New Content'}
              </Button>
           </label>
        </div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
         <StatCard label="Total Ingested" value={files.length} icon={Database} color="text-aura" />
         <StatCard label="Storage Status" value="OPTIMAL" icon={CheckCircle2} color="text-emerald-500" />
         <StatCard label="Pipeline Latency" value="1.2s" icon={Loader2} color="text-highlight" />
      </div>

      <Card className="p-10 space-y-10 border-slate-900 bg-slate-950/20">
         <div className="flex justify-between items-center">
            <h3 className="text-2xl font-black text-white uppercase tracking-tight">Knowledge Repository</h3>
            <div className="relative w-64">
               <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" size={16} />
               <input
                  type="text"
                  placeholder="Search repository..."
                  className="w-full bg-slate-900 border border-slate-800 rounded-xl py-2 pl-10 pr-4 text-xs focus:border-aura outline-none"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
               />
            </div>
         </div>

         <div className="space-y-4">
            {filteredFiles.map((file) => (
              <div key={file.file_id} className="p-6 rounded-3xl bg-slate-950 border border-slate-900 flex items-center justify-between group hover:border-aura/30 transition-all">
                 <div className="flex items-center gap-6">
                    <div className="w-12 h-12 rounded-xl bg-slate-900 flex items-center justify-center text-aura group-hover:scale-110 transition-transform">
                       <FileText size={24} />
                    </div>
                    <div>
                       <p className="text-sm font-black text-white uppercase tracking-widest">{file.filename}</p>
                       <p className="text-[10px] text-slate-500 font-bold uppercase">
                          {file.content_type} • {(file.size / 1024).toFixed(1)} KB • Ingested {new Date(file.timestamp).toLocaleString()}
                       </p>
                    </div>
                 </div>
                 <div className="flex items-center gap-4">
                    <Badge color="emerald-500">{file.status}</Badge>
                    <Button variant="outline" className="px-4 py-2 text-[8px] uppercase font-black" onClick={() => alert(file.extracted_text)}>View Extract</Button>
                    <button className="text-slate-700 hover:text-vital transition-colors">
                       <Trash2 size={16} />
                    </button>
                 </div>
              </div>
            ))}
            {filteredFiles.length === 0 && (
              <div className="text-center py-20">
                 <p className="text-slate-500 font-bold uppercase tracking-widest text-xs">No content found in the mesh.</p>
              </div>
            )}
         </div>
      </Card>
    </div>
  );
};

const StatCard = ({ label, value, icon: Icon, color }: any) => (
  <Card className="p-6 flex items-center gap-6 bg-slate-950/40 border-slate-900">
     <div className={`p-4 rounded-2xl bg-slate-900 border border-slate-800 ${color}`}>
        <Icon size={24} />
     </div>
     <div>
        <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
        <p className="text-2xl font-black text-white">{value}</p>
     </div>
  </Card>
);
