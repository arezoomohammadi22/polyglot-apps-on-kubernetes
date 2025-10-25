# Flask + PostgreSQL on Kubernetes

This project demonstrates deploying a simple **Flask REST API** with a **PostgreSQL** backend on **Kubernetes**, using ConfigMap and Secret for environment configuration.

---

## 📁 Project Structure

```
myapplication/
│
├── app/
│   ├── app.py
│   ├── db.py
│   └── requirements.txt
│
├── Dockerfile
│
└── k8s/
    ├── configmap.yaml
    ├── secret.yaml
    ├── db-deployment.yaml
    └── app-deployment.yaml
```

---

## ⚙️ 1. Build and Push Docker Image

Build the image locally (replace `v4` with your desired tag):
```bash
docker build -t flask-k8s-demo:v4 .
```

Optionally, push to your registry:
```bash
docker tag flask-k8s-demo:v4 <your-registry>/flask-k8s-demo:v4
docker push <your-registry>/flask-k8s-demo:v4
```

---

## ☁️ 2. Apply Kubernetes Manifests

Create ConfigMap and Secret:
```bash
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml
```

Deploy PostgreSQL and Service:
```bash
kubectl apply -f k8s/db-deployment.yaml
```

Deploy Flask App and Service:
```bash
kubectl apply -f k8s/app-deployment.yaml
```

Verify all resources are running:
```bash
kubectl get pods,svc
```

---

## 🧪 3. Test the Application

### Port-forward to access the Flask service:

```bash
kubectl port-forward svc/flask-service 8080:80
```

### Get all users:
```bash
curl http://localhost:8080/users
```

Expected response (initially empty):
```json
[]
```

### Add a new user:
```bash
curl -X POST http://localhost:8080/users      -H "Content-Type: application/json"      -d '{"name": "Alice"}'
```

Response:
```json
{"message": "user 'Alice' created"}
```

### List users again:
```bash
curl http://localhost:8080/users
```
Expected response:
```json
[{"id": 1, "name": "Alice"}]
```

---

## 🧩 4. Inspect the Database

Connect to PostgreSQL pod:
```bash
kubectl exec -it $(kubectl get pod -l app=postgres -o name) -- bash
```

Inside the pod:
```bash
psql -U flaskuser -d flaskdb
\dt
SELECT * FROM users;
```

---

## 🧰 5. Environment Variables Mapping

| Source | Key | Used in Code |
|---------|-----|--------------|
| ConfigMap | DB_HOST | host |
| ConfigMap | DB_NAME | database |
| Secret | DB_USER | user |
| Secret | DB_PASSWORD | password |

Flask reads these variables inside `db.py` via `os.environ.get()` to connect to PostgreSQL.

---

## 🧹 6. Cleanup

To remove all resources:
```bash
kubectl delete -f k8s/app-deployment.yaml
kubectl delete -f k8s/db-deployment.yaml
kubectl delete -f k8s/configmap.yaml
kubectl delete -f k8s/secret.yaml
```

---

## ✅ Summary

- Flask REST API connects to PostgreSQL database using psycopg2.
- ConfigMap and Secret manage configuration and credentials.
- Application and database both run as separate Kubernetes Deployments.
- Easily test via port-forwarding and `curl` commands.

---

**Author:** Arezoo Begmohammadi 
**Version:** v4
