"""
CommitClub - Integração com Google Gemini API
Gera roadmaps de estudo personalizados em formato JSON.
"""

import json
import os
from django.conf import settings

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


def configurar_gemini():
    """Configura a API do Gemini com a chave do .env"""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada no .env")
    genai.configure(api_key=api_key)


def gerar_roadmap(tema, nivel='iniciante', duracao_semanas=4):
    """
    Gera um roadmap de estudo personalizado usando Gemini.
    
    Args:
        tema: Tema do roadmap (ex: 'Python', 'React', 'Machine Learning')
        nivel: Nível do estudante ('iniciante', 'intermediario', 'avancado')
        duracao_semanas: Duração do roadmap em semanas
    
    Returns:
        dict: Roadmap estruturado em JSON
    """
    if not GENAI_AVAILABLE:
        return _roadmap_fallback(tema, nivel, duracao_semanas)
    
    try:
        configurar_gemini()
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"""
        Crie um roadmap de estudo detalhado para aprender {tema}.
        Nível do estudante: {nivel}
        Duração: {duracao_semanas} semanas
        
        Retorne APENAS um JSON válido (sem markdown) no seguinte formato:
        {{
            "titulo": "Roadmap de {tema}",
            "nivel": "{nivel}",
            "duracao_semanas": {duracao_semanas},
            "descricao": "Descrição breve do roadmap",
            "semanas": [
                {{
                    "numero": 1,
                    "titulo": "Título da semana",
                    "objetivos": ["objetivo 1", "objetivo 2"],
                    "tarefas": [
                        {{
                            "titulo": "Nome da tarefa",
                            "descricao": "O que fazer",
                            "tipo": "leitura|pratica|projeto",
                            "tempo_estimado": "2h"
                        }}
                    ],
                    "recursos": ["link ou referência 1", "link ou referência 2"]
                }}
            ],
            "projeto_final": {{
                "titulo": "Nome do projeto",
                "descricao": "Descrição do projeto final",
                "requisitos": ["requisito 1", "requisito 2"]
            }}
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Limpar resposta e extrair JSON
        text = response.text.strip()
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]
        
        roadmap = json.loads(text)
        return roadmap
        
    except Exception as e:
        print(f"Erro ao gerar roadmap com Gemini: {e}")
        return _roadmap_fallback(tema, nivel, duracao_semanas)


def _roadmap_fallback(tema, nivel, duracao_semanas):
    """Roadmap de fallback quando a API não está disponível."""
    return {
        "titulo": f"Roadmap de {tema}",
        "nivel": nivel,
        "duracao_semanas": duracao_semanas,
        "descricao": f"Plano de estudo para {tema} no nível {nivel}.",
        "semanas": [
            {
                "numero": i + 1,
                "titulo": f"Semana {i + 1} - Fundamentos" if i < duracao_semanas // 2 else f"Semana {i + 1} - Prática Avançada",
                "objetivos": [
                    f"Estudar conceitos da semana {i + 1}",
                    f"Praticar exercícios de {tema}"
                ],
                "tarefas": [
                    {
                        "titulo": f"Estudo teórico - Semana {i + 1}",
                        "descricao": f"Estudar os fundamentos de {tema} referentes à semana {i + 1}",
                        "tipo": "leitura",
                        "tempo_estimado": "3h"
                    },
                    {
                        "titulo": f"Exercícios práticos - Semana {i + 1}",
                        "descricao": f"Resolver exercícios práticos de {tema}",
                        "tipo": "pratica",
                        "tempo_estimado": "4h"
                    }
                ],
                "recursos": [
                    f"Documentação oficial de {tema}",
                    f"Tutoriais e vídeos sobre {tema}"
                ]
            }
            for i in range(duracao_semanas)
        ],
        "projeto_final": {
            "titulo": f"Projeto Final de {tema}",
            "descricao": f"Desenvolver um projeto completo aplicando tudo que foi aprendido sobre {tema}.",
            "requisitos": [
                "Aplicar os conceitos aprendidos",
                "Documentar o código",
                "Publicar no GitHub"
            ]
        }
    }
