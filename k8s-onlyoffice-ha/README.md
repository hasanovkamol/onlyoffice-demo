# ONLYOFFICE Document Server HA on Kubernetes

Ushbu loyiha ONLYOFFICE Document Serverni Kubernetes (K8s) klasterida **High Availability (HA)** va **Stateless** arxitektura asosida loyihalash uchun mo'ljallangan.

## 🏗 Arxitektura Xususiyatlari
- **Stateless Design**: Barcha ma'lumotlar tashqi bazalarda va Shared Storage'da saqlanadi.
- **Microservices**: `DocService` va `FileConverter` alohida deployment sifatida ajratilgan va masshtablanadi (Scaling).
- **Sticky Sessions**: Nginx Ingress orqali sessiya barqarorligi taminlangan.
- **Monitoring**: Prometheus, Grafana va Seq integratsiyasi mavjud.

## 📂 Loyiha Tuzilmasi
```text
k8s-onlyoffice-ha/
├── base/               # Global resurslar (PVC, Secrets)
├── infrastructure/     # Ma'lumotlar bazasi va Broker (Postgres, RabbitMQ)
├── monitoring/         # Kuzatuv tizimi (Seq, Prometheus, Grafana)
├── onlyoffice/         # Custom OnlyOffice komponentlari va Ingress
└── apps/               # Asosiy WebApi ilovasi
```

## 🚀 O'rnatish Tartibi (Deployment)

Loyihani klasterga tatbiq etish uchun quyidagi ketma-ketlikda buyruqlarni bajaring:

### 1. Umumiy sozlamalar va Storage
```bash
kubectl apply -f base/pvc.yaml
```

### 2. Infratuzilmani ishga tushirish
```bash
kubectl apply -f infrastructure/database.yaml
kubectl apply -f infrastructure/rabbitmq.yaml
```

### 3. Monitoring tizimi
```bash
kubectl apply -f monitoring/stack.yaml
```

### 4. ONLYOFFICE va WebApi komponentlari
```bash
kubectl apply -f onlyoffice/deployment-docservice.yaml
kubectl apply -f onlyoffice/deployment-fileconverter.yaml
kubectl apply -f onlyoffice/ingress.yaml
kubectl apply -f apps/webapi.yaml
```

## ⚙️ Shaxsiy sozlamalar (Customization)
- **Image**: `onlyoffice/` va `apps/` papkalaridagi YAML fayllarda `image:` qatorini o'zingizning Docker Hub'dagi custom image manzilingiz bilan almashtiring.
- **Storage**: `base/pvc.yaml`da o'zingizning `storageClassName` (NFS, Ceph va h.k.) ni ko'rsating.
- **Domain**: `onlyoffice/ingress.yaml` faylida `host:` qismiga o'z domeningizni yozing.

## 📊 Monitoring Endpointlar
- **OnlyOffice Health**: `http://<domain>/healthcheck`
- **Grafana**: `http://monitoring-svc:3000`
- **Prometheus**: `http://monitoring-svc:9090`
- **Seq Logs**: `http://monitoring-svc:5341`

## 🛡 Xavfsizlik bo'yicha tavsiyalar
- `database.yaml` faylidagi parollarni `Secrets` ob'ektiga ko'chirish tavsiya etiladi.
- Ingress uchun **TLS (SSL)** sertifikatlarini o'rnating.
