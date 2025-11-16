# Python App + Postgres Helm Deployment  
This project deploys **Flask App** + **Postgres Database** using **one Helm chart**, including:  
- Flask Deployment + Service  
- Postgres Deployment + Service  
- ConfigMap for app configuration  
- SealedSecrets for both app & database secrets  
- Instructions for generating encrypted SealedSecrets  

---

# 📌 Prerequisites
- Kubernetes cluster
- Helm v3+
- Bitnami SealedSecrets controller installed:

```bash
helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
helm install sealed-secrets-controller sealed-secrets/sealed-secrets   --namespace kube-system
```

---

# 📁 Project Structure

```
python-app/
  Chart.yaml
  values.yaml
  templates/
    deployment-app.yaml
    service-app.yaml
    configmap.yaml
    sealedsecret-app.yaml
    postgres-deployment.yaml
    postgres-service.yaml
    postgres-sealedsecret.yaml
```

Everything deploys with **one helm install**.

---

# 🔐 Creating SealedSecrets

SealedSecrets allow you to store secrets inside Git safely because they become encrypted.  
Only the cluster’s SealedSecret controller can decrypt them.

Below are the exact commands for generating the encrypted secrets used in this project.

---

# 1️⃣ Postgres SealedSecret

## Step 1 — Create raw secret manifest

```bash
kubectl -n devops create secret generic postgres-secret   --from-literal=POSTGRES_DB='flaskdb'   --from-literal=POSTGRES_USER='flaskuser'   --from-literal=POSTGRES_PASSWORD='strongpassword123'   --dry-run=client -o yaml > postgres-secret-raw.yaml
```

## Step 2 — Convert to SealedSecret

```bash
kubeseal   --format=yaml   --controller-name=sealed-secrets-controller   --controller-namespace=kube-system   < postgres-secret-raw.yaml > postgres-sealed-secret.yaml
```

## Step 3 — Extract encrypted values

```bash
cat postgres-sealed-secret.yaml
```

Look under:

```
spec:
  encryptedData:
    POSTGRES_DB: AgAAAA...
    POSTGRES_USER: AgBBBB...
    POSTGRES_PASSWORD: AgCCCC...
```

Copy these values into:

```yaml
postgresSealedSecrets:
  db: "AgAAAA..."
  user: "AgBBBB..."
  password: "AgCCCC..."
```

inside your chart’s `values.yaml`.

---

# 2️⃣ App (Flask) SealedSecret

## Step 1 — Create raw app secret

```bash
kubectl -n devops create secret generic app-secret   --from-literal=DB_USER='flaskuser'   --from-literal=DB_PASSWORD='strongpassword123'   --dry-run=client -o yaml > secret-raw.yaml
```

## Step 2 — Convert to SealedSecret

```bash
kubeseal   --format=yaml   --controller-name=sealed-secrets-controller   --controller-namespace=kube-system   < secret-raw.yaml > sealed-secret-generated.yaml
```

## Step 3 — Extract encrypted values

```bash
cat sealed-secret-generated.yaml
```

Find:

```
spec:
  encryptedData:
    DB_USER: AgDDD...
    DB_PASSWORD: AgEEE...
```

Copy into:

```yaml
sealedSecrets:
  dbUser: "AgDDD..."
  dbPassword: "AgEEE..."
```

inside your chart’s `values.yaml`.

---

# 🧩 Setting DB_HOST in the ConfigMap

Inside `configmap.yaml` your app will use:

```yaml
data:
  DB_HOST: "postgres"
  DB_NAME: "flaskdb"
```

Because the internal Service of Postgres is named:

```
postgres
```

---

# 🚀 Deploying Everything With Helm

After adding encrypted values to `values.yaml`, install everything with:

```bash
helm upgrade --install python-app ./python-app   --namespace devops   --create-namespace
```

This will create:

### Flask App
- Deployment
- ClusterIP Service
- ConfigMap
- app-secret (from SealedSecret)

### Postgres
- Deployment
- ClusterIP Service
- postgres-secret (from SealedSecret)

---

# ✔️ Verify Secrets Created Successfully

```bash
kubectl -n devops get sealedsecret
kubectl -n devops get secret | grep postgres
kubectl -n devops get secret | grep app
```

---

# ✔️ Verify Pods

```bash
kubectl -n devops get pods
```

---

# ✔️ Verify Services

```bash
kubectl -n devops get svc
```

---

# 🎉 Done!

