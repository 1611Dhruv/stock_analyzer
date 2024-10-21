### **Project Overview**

This Django application serves as a financial data analysis platform, offering functionalities such as:

- Fetching historical stock data from Alpha Vantage API
- Storing data in a PostgreSQL database
- Backtesting simple buy/sell strategies
- Integrating a pre-trained machine learning model for stock price prediction
- Generating comprehensive reports

**Prerequisites**

- Python 3.x
- pip
- git
- Docker (recommended)

**Installation**

1. **Clone the Repository:**

   ```bash
   git clone https://<your_repository_url>
   ```

2. **Configure Environment Variables:**

   - Create a `.env` file in the project root directory.
   - Add your Alpha Vantage API key:
     ```
     ALPHA_VANTAGE_API_KEY=<your_api_key>
     ```

3. **Install Dependencies:**

   - Invoke the `startup` script in the project root directory.
   - Make sure to invoke it using the `. ./startup` command so that the environment changes get applied to your current shell session

   ```bash
   . ./startup
   ```

   **Running the Application**

4. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

**API Endpoints**

- **Financial Data:**
  - `POST /financial_data/add`: Add a new stock symbol. It expects the `symbol` parameter in the request body.
  - `POST /financial_data/refresh`: Refresh data for existing symbols
  - `GET /financial_data/data`: List available symbols
  - `GET /financial_data/data?symbol=<symbol>`: Get data for a specific symbol
- **Backtesting:**
  - `GET /back_test?format=<pdf|json>&symbol=<symbol>&winsell=<sell_threshold>&winbuy=<buy_threshold>`: Perform backtesting
- **AI Prediction:**
  - `GET /ai_prediction?symbol=<symbol>`: Get predicted prices
- **Reporting:**
  - Access the reporting interface at `/reporting/`

**Deployment**

- **Dockerize:** Create a Dockerfile to package the application.
- **Configure Cloud Provider:** Set up AWS or another cloud provider with necessary resources (e.g., EC2, S3, RDS).
- **Deploy:** Use tools like `docker-compose` or CI/CD pipelines to deploy the containerized application.

**Evaluation Criteria**

- **API Integration:** Efficient data fetching and handling.
- **Backtesting Logic:** Accurate calculations and performance metrics.
- **ML Integration:** Seamless model integration and prediction accuracy.
- **Reporting:** Clear visualizations and metrics.
- **Deployment:** Production-ready setup and scalability.
- **Documentation:** Comprehensive README and clear instructions.

**Additional Notes**

- Ensure the `startup` script handles environment setup and dependency installation.
- Consider using a secrets management tool to store sensitive information like API keys.
- Provide detailed instructions for deployment, including configuration and deployment scripts.

By following these steps and adhering to the evaluation criteria, you can successfully complete the Django Backend Engineer Trial Task.
