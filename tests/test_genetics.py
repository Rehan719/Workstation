import asyncio
from agentic_core.pulse.pulse_clock import PulseClock
from agentic_core.genetics.genome_encoder import GenomeEncoder
from agentic_core.genetics.transcription_engine import TranscriptionEngine
from agentic_core.genetics.translation_engine import TranslationEngine

async def test_central_dogma_engine():
    clock = PulseClock()
    encoder = GenomeEncoder()
    transcriber = TranscriptionEngine(clock)
    translator = TranslationEngine()

    # 1. Encoding (DNA)
    gene = encoder.encode_article("CA-I", "Implement Central Dogma Engine", {"threshold": 0.3})
    assert gene["gene_id"] == "CA-I"

    # 2. Transcription (RNA)
    signals = {"allostatic_load": 2.0}
    rna = transcriber.transcribe(gene, signals)
    assert rna is not None
    assert rna["transcript_id"].startswith("RNA_CA-I")

    # 3. Translation (Protein)
    protein = translator.translate(rna)
    assert protein is not None
    assert protein["protein_id"].startswith("PROT_RNA_CA-I")

    print("Central Dogma Engine verification PASSED.")

if __name__ == "__main__":
    asyncio.run(test_central_dogma_engine())
