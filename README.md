**🧠 MultiAgent Clinical AI**

A **multi-agent clinical decision support system** built using **LangGraph** that simulates structured medical reasoning.

The system takes raw patient input and processes it through multiple specialized agents to generate, validate, and refine differential diagnoses in an iterative loop.

---

## **🚀 Features**

* Multi-agent architecture (Scribe → Diagnostic → Validator → Critic)  
* Structured extraction of clinical data from raw text  
* Ranked differential diagnosis generation  
* Evidence-based validation with safety checks  
* Iterative refinement loop for improved output quality  
* Modular and extensible design

---

## 

## 

## 

## 

## **🧠 System Architecture**

The system is built as a **graph-based workflow** using LangGraph:

Patient Input  
     ↓  
Scribe Agent → Extract structured data  
     ↓  
Diagnostic Agent → Generate differential diagnoses  
     ↓  
Validator Agent → Evaluate evidence & safety  
     ↓  
Critic Agent → Score quality & decide (approve / refine)  
     ↓  
   Loop (if needed)  
     ↓  
Final Output

---

## **🧩 Agents Overview**

### **1\. Scribe Agent**

* Converts raw patient input into structured medical data  
* Extracts symptoms, history, medications, and key findings

### **2\. Diagnostic Agent**

* Generates a ranked list of possible diagnoses (DDx)  
* Uses clinical reasoning based on structured data

### **3\. Validator Agent**

* Evaluates each diagnosis for:  
  * Medical plausibility  
  * Evidence strength  
  * Safety risks (e.g., drug interactions)  
* Produces an evidence report and safety report

### **4\. Critic Agent**

* Assigns a quality score  
* Decides whether to:  
  * **Approve** the result  
  * **Refine** (loop back for improvement)

---

## **⚙️ Setup Instructions**

### **1\. Clone the Repository**

git clone https://github.com/abdullah-codez/multiagent-clinical-ai.git  
cd multiagent-clinical-ai

---

### **2\. Create Virtual Environment**

python \-m venv venv  
venv\\Scripts\\activate   \# Windows

---

### **4\. Setup Environment Variables**

Create a .env file in the root directory:

GEMINI\_API\_KEY=your\_api\_key\_here  
---

### **5\. Model Configuration**

Each agent uses an LLM internally. You can **choose or change the model inside each agent file** depending on your needs.

Example:

model \= genai.GenerativeModel("gemini-2.5-flash")

👉 You may switch to lighter or more powerful models depending on:

* API limits  
* cost  
* performance requirements

---

## **▶️ Running the Project**

python main.py

The system will process the sample patient input and output:

* Differential Diagnosis  
* Evidence Report  
* Safety Report  
* Quality Score  
* Iteration Count

---

## **📊 Example Output**

* Ranked diagnoses with reasoning  
* Evidence-based validation scores  
* Safety warnings and red flags  
* Final decision after refinement loop

---

## **⚠️ Disclaimer**

This project is for **educational and experimental purposes only**.  
It is **not a medical tool** and should not be used for real clinical decision-making.

---

## **🔮 Future Improvements**

* Integrate RAG for evidence retrieval (WHO, PubMed, etc.)  
* Add real clinical datasets  
* Improve scoring and evaluation metrics  
* Deploy as a web application  
* Add explainability layer for decisions

---

## **🧑‍💻 Author**

Muhammad Abdullah Iftikhar  
Computer Science Undergraduate | ML Enthusiast

---

