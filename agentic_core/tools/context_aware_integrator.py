from typing import Any, Dict, List, Optional
from .task_classifier import TaskClassifier
from .mlir_engine import MLIREngine
from .qir_engine import QIREngine
from .sigstore_engine import SigstoreEngine

class ContextAwareToolIntegrator:
    """
    Selectively activates advanced toolchains based on task context (Article T).
    MLIR/QIR for complex algorithms; Sigstore for artifact signing.
    """
    def __init__(self):
        self.task_classifier = TaskClassifier()
        self.mlir_engine = MLIREngine()
        self.qir_engine = QIREngine()
        self.sigstore_engine = SigstoreEngine()
        self.activation_log = []

    async def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task with selective toolchain activation."""
        classification = await self.task_classifier.classify(task)
        result = {'status': 'processed', 'tools_used': []}

        # MLIR/QIR Activation
        if classification['complexity'] in ['high', 'medium'] and classification.get('quantum'):
            optimized = await self.mlir_engine.optimize(task.get('circuit'))
            qir = await self.qir_engine.generate(optimized)
            result['circuit_qir'] = qir
            result['tools_used'].append('mlir_qir')

        # Sigstore Activation
        if task.get('produces_artifact'):
            signature = await self.sigstore_engine.sign(task.get('artifact_data', {}))
            result['signature'] = signature
            result['tools_used'].append('sigstore')

        self.activation_log.append({
            'task_id': task.get('id'),
            'classification': classification,
            'tools': result['tools_used']
        })

        return result
