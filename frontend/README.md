<<<<<<< HEAD
# CANON – Customer Alert & Notification Orchestration Network

**CANON** is a lightweight microservice-based platform that captures "Contact Us" form submissions, processes them via Kafka, stores them in PostgreSQL, and sends real-time email notifications to customers. Built with FastAPI, Kafka, and React, CANON is ideal for businesses looking to streamline and scale customer communication workflows.

---

## 🔧 Key Features

- 📬 Frontend form built with **React**
- ⚙️ Backend powered by **FastAPI**
- 🧵 Asynchronous messaging using **Kafka**
- 🗃️ Persistent storage via **PostgreSQL**
- 🔐 Credential management via `.env` (KMS integration planned)
- 📧 Email notifications via **SMTP**
- 🧪 Local dev with `venv`, live-reloading, and Kafka CLI tools

---

## 📁 Project Structure

FS_Project/
├── frontend/         # React UI for form submission
├── microservice1/    # FastAPI producer service (form ingestion)
├── microservice2/    # Kafka consumer & email sender
└── README.md


---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/fs-project.git
cd fs-project




cd frontend
npm install
npm start



cd ../microservice1
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload


cd ../microservice2
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 consumer.py

microservice1/.env
DB_URL=postgresql://<db_user>:<db_password>@localhost:5432/<db_name>
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=form-submissions

microservice2/.env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
TOPIC_NAME=form-submissions
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=<your_email>
SENDER_PASSWORD=<your_app_password>
=======
# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
>>>>>>> 455540d (Initialize project using Create React App)
