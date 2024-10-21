# AquaData 🌊

AquaData is a Streamlit application that provides information about water quality in the main surface water bodies of Mexico. It includes a chatbot powered by Groq AI to answer questions based on the aquatic data.

## Setup and Deployment

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/your-username/aquadata.git
   cd aquadata
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.env` file in the root directory of the project.
   - Add your Groq API key to the `.env` file:
     ```
     GROQ_API_KEY=your-api-key-here
     ```

4. Run the Streamlit app locally:
   ```
   streamlit run --server.environment=.env streamlit_app.py
   ```

### Deployment on Streamlit Cloud

1. Fork this repository to your GitHub account.

2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud) if you haven't already.

3. Create a new app in Streamlit Cloud and connect it to your forked GitHub repository.

4. In the app's settings on Streamlit Cloud:
   - Set the Python version to 3.9 or higher.
   - Add the following secret:
     - Key: `GROQ_API_KEY`
     - Value: Your Groq API key

5. Deploy the app. Streamlit Cloud will automatically install the dependencies from `requirements.txt`.

## Security Notes

- Never commit your `.env` file or expose your API keys in the code.
- The `.gitignore` file is set up to exclude `.env` and `.streamlit/secrets.toml` to prevent accidental commits of sensitive information.
- When deploying to Streamlit Cloud, always use the secrets management feature to securely store your API keys.

## Data Source

The application uses the `AquaData.csv` file as its data source. Ensure this file is present in the root directory of the project.

## Credits

- Idea and RAG implementation: Gibrann Morgado
- Data Transformation: Daniel Carmona and Jossimar Morgado
- Strategic Design: Sofia Garcia Conde

For questions or inquiries, please contact: contact@immanentize.cc
