import streamlit as st
import pandas as pd
import groq
import os

# Check if the API key is set
if "GROQ_API_KEY" not in os.environ and "GROQ_API_KEY" not in st.secrets:
    st.error("GROQ_API_KEY is not set. Please set it as an environment variable or in Streamlit secrets.")
    st.stop()

# Initialize Groq client
client = groq.Groq(api_key=os.environ.get("GROQ_API_KEY") or st.secrets["GROQ_API_KEY"])

# Function to load data from CSV
@st.cache_data
def load_csv_data(file_path):
    return pd.read_csv(file_path)

# Function to check if question is water-related
def is_water_related(question):
    water_keywords = [
        # Cuerpos de agua
        'agua', 'water', 'lago', 'lake', 'río', 'river', 'laguna', 'pond', 
        'arroyo', 'stream', 'presa', 'dam', 'embalse', 'reservoir',
        'manantial', 'spring', 'costa', 'coast', 'mar', 'sea',
        
        # Calidad y parámetros
        'calidad', 'quality', 'ph', 'hidric', 'hídric',
        'contamin', 'pollution', 'turbidez', 'turbidity',
        'temperatura', 'temperature', 'oxígeno', 'oxygen',
        'conductividad', 'conductivity', 'sediment', 'sedimento',
        
        # Limpieza y tratamiento
        'limpi', 'clean', 'tratamiento', 'treatment', 'purific',
        'filtr', 'filter', 'desinfec', 'disinfect', 'potabil',
        'sanea', 'sanit', 'depura', 'purify',
        
        # Usos prácticos
        'consumo', 'consumption', 'beber', 'drinking',
        'riego', 'irrigation', 'agricultura', 'agriculture',
        'industrial', 'industry', 'recreativ', 'recreational',
        'pesca', 'fishing', 'nadar', 'swimming', 'navegación',
        'doméstico', 'domestic', 'potable', 'portable',
        
        # Mantenimiento y conservación
        'manteni', 'maintenance', 'conserva', 'conservation',
        'restaurar', 'restoration', 'rehabilita', 'rehabilitation',
        'preserva', 'preserve', 'proteg', 'protect',
        
        # Problemas y soluciones
        'erosión', 'erosion', 'residuo', 'waste',
        'basura', 'trash', 'contamina', 'pollut',
        'vertido', 'discharge', 'derrame', 'spill'
    ]
    return any(keyword.lower() in question.lower() for keyword in water_keywords)

# Function to generate response using Groq API
def generate_response(prompt, context):
    if not is_water_related(prompt):
        return "Lo siento, solo puedo responder preguntas relacionadas con la calidad del agua, cuerpos de agua y sus usos prácticos. Por favor, reformula tu pregunta para que se relacione con estos temas."

    system_prompt = """You are a specialized water quality data assistant with expertise in practical water uses and water body management. You answer questions about:

1. Water Quality & Parameters:
   - Water quality measurements and standards
   - Physical, chemical, and biological parameters
   - Contamination levels and their implications

2. Water Bodies:
   - Lakes, rivers, ponds, streams, reservoirs
   - Coastal waters and marine environments
   - Natural springs and groundwater

3. Cleaning & Treatment:
   - Water body cleaning methods
   - Treatment processes and technologies
   - Purification and filtration systems
   - Maintenance and restoration practices

4. Practical Uses:
   - Drinking water requirements
   - Agricultural irrigation
   - Industrial applications
   - Recreational activities (swimming, fishing)
   - Domestic use considerations

5. Conservation & Management:
   - Environmental protection
   - Ecosystem preservation
   - Sustainable water use
   - Pollution prevention

Base your answers on the provided context data and focus on practical, actionable information. If discussing cleaning or treatment, include relevant quality parameters and standards. For practical uses, consider safety requirements and quality thresholds.

Remember: Provide specific, practical advice while maintaining technical accuracy."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}"}
    ]
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.2-3b-preview",
        max_tokens=250,
        temperature=0.7,
    )
    
    return chat_completion.choices[0].message.content

# Streamlit app
def main():
    st.title("AquaData 🌊")

    st.write("""
    La información sobre calidad hídrica está dispersa en múltiples fuentes y formatos.

    Las bases de datos existentes son complejas, difíciles de consultar y presentan inconsistencias en su estructura y contenido. Esto afecta la gobernanza, el monitoreo ambiental y las cadenas de valor relacionadas con los recursos hídricos.

    AQUADATA una base de datos centralizada sobre la calidad del agua en los principales cuerpos superficiales de México. Esta base servirá para calibrar imágenes satelitales, mejorando estimaciones de parámetros hídricos a gran escala. Además de haber generado esta base de datos (cleansing, normalización,PCA) creamoos un RAG AI que interactúa con esta base de conocimieto através de un chat.

    Áreas de impacto:  seguridad hídrica, eficiencia industrial, y cadenas de valor, promoviendo transparencia y acceso a la información. Beneficiará a sectores públicos y privados, apoyando el desarrollo de Sistemas de Monitoreo, Reporte y Verificación (MRV) para la gestión económica y ecológica de cuencas.""")

    # Load CSV data
    csv_file = "AquaData.csv"
    try:
        data = load_csv_data(csv_file)
    except FileNotFoundError:
        st.error(f"CSV file '{csv_file}' not found. Please make sure 'AquaData.csv' exists in the same directory as the app.")
        st.stop()

    # Add dropdown to filter by ESTADO
    st.header("Filtra por estado")
    estados = ['All'] + sorted(data['ESTADO'].unique().tolist())
    selected_estado = st.selectbox("Select a state:", estados)

    # Filter and display data based on selection
    if selected_estado != 'All':
        filtered_data = data[data['ESTADO'] == selected_estado]
    else:
        filtered_data = data

    st.subheader("Filtered Data")
    st.dataframe(filtered_data)

    # Function to truncate context
    def truncate_context(context, max_chars=12000):  # Approx. 3000 tokens
        if len(context) <= max_chars:
            return context
        return context[:max_chars]

    # Chatbot interface
    st.header("AquaData Chatbot")
    st.write("""Este chatbot está especializado en responder preguntas sobre:
    - Calidad del agua y parámetros hídricos
    - Limpieza y tratamiento de cuerpos de agua
    - Usos prácticos del agua (consumo, agricultura, recreación)
    - Conservación y mantenimiento de recursos hídricos""")
    with st.container():
        user_input = st.text_area("Haz una pregunta sobre calidad del agua, limpieza de cuerpos de agua o usos prácticos:", height=100)
        if st.button("Send"):
            if user_input:
                # Convert filtered data to string and truncate to approx. 3000 tokens
                full_context = filtered_data.to_string()
                truncated_context = truncate_context(full_context)
                
                with st.spinner("Generating response..."):
                    response = generate_response(user_input, truncated_context)
                st.subheader("Chatbot Response:")
                st.write(response)
            else:
                st.warning("Please enter a question.")
    st.write("Fuentes: **CONAGUA** (Comisión Nacional del Agua), Red Nacional de Medición de Calidad del Agua (RENAMECA), SEMARNAT")
    st.write("Créditos: Idea e implementación de RAG: Gibrann Morgado, Transformación de Data: Daniel Carmona y Jossimar Morgado, Strategic design: Sofia Garcia Conde .Preguntas: contact@immanentize.cc")

if __name__ == "__main__":
    main()

