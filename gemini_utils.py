import os
import json
import logging

logger = logging.getLogger(__name__)

def gerar_roadmap_desafio(titulo, duracao_dias, nivel='Iniciante'):
    """
    Gera um roadmap de aprendizado estruturado usando a API do Gemini.
    Retorna um JSON serializado se bem sucedido, ou um Mock pre-determinado se falhar/não configurado.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    
    if api_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            prompt = f"""
            Você é um tech lead criando um roadmap prático para um desenvolvedor {nivel}.
            O objetivo é aprender "{titulo}" em {duracao_dias} dias.
            Retorne APENAS um JSON válido contendo semanas e tarefas diárias. O formato DEVE ser exato:
            {{
                "semanas": [
                    {{
                        "titulo": "Semana 1 - Fundamentos",
                        "descricao": "Conceitos básicos",
                        "dias": [
                            {{"dia": 1, "tarefa": "Instalação e Hello World", "concluido": false}},
                            {{"dia": 2, "tarefa": "Sintaxe básica", "concluido": false}}
                        ]
                    }}
                ]
            }}
            """
            response = model.generate_content(prompt)
            # Tentar extrair o JSON puro caso venha com blocos de código Markdown
            text = response.text.strip()
            if text.startswith('```json'):
                text = text.replace('```json', '', 1)
            if text.endswith('```'):
                text = text[:-3]
            
            return json.loads(text.strip())
        except Exception as e:
            logger.error(f"Erro ao gerar roadmap com Gemini: {str(e)}")
            # Fallback para o Mock
            pass

    # Mock Data para interface imediata (Business Plan UI)
    semanas_mock = []
    dias_por_semana = 7
    total_semanas = (int(duracao_dias) + dias_por_semana - 1) // dias_por_semana

    for s in range(1, total_semanas + 1):
        dias = []
        for d in range(1, dias_por_semana + 1):
            dia_geral = (s - 1) * dias_por_semana + d
            if dia_geral <= int(duracao_dias):
                dias.append({
                    "dia": dia_geral,
                    "tarefa": f"Conceito {dia_geral} - Prática e exercícios",
                    "concluido": False
                })
        
        titulo_semana = "Fundamentos" if s == 1 else "Avançando" if s == 2 else "Projeto Final"
        semanas_mock.append({
            "titulo": f"Semana {s} - {titulo_semana}",
            "descricao": "Tópicos de estudo focados.",
            "dias": dias
        })

    return {"semanas": semanas_mock}
