from dataclasses import dataclass


@dataclass
class LLMSettings:
    provider: str
    model: str
    temperature: float
    max_tokens: int


@dataclass
class ChunkingSettings:
    chunk_size: int
    overlap: int


@dataclass
class StandardizationSettings:
    enabled: bool
    use_llm_for_entities: bool


@dataclass
class InferenceSettings:
    enabled: bool
    use_llm_for_inference: bool
    apply_transitive: bool


@dataclass
class VisualizationSettings:
    directed: bool
    show_edge_labels: bool
    output_file: str


@dataclass
class Settings:
    llm: LLMSettings
    chunking: ChunkingSettings
    standardization: StandardizationSettings
    inference: InferenceSettings
    visualization: VisualizationSettings
