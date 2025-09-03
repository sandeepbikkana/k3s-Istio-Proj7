# Canary Deployment Project (K3s + Istio + Docker + Helm)

Contents:
- `app/nodejs/` - Node.js demo app (v1/v2 tag is set via Kubernetes env)
- `app/python/` - Python demo app (Flask) alternative
- `k8s-yaml/` - Raw YAML manifests you can apply directly to K3s (namespace, deployments, service, istio configs)
- `chart/demo-canary/` - Helm chart to deploy the app + Istio configs and control traffic weights via values
- `strategy.md` - Canary deployment strategy document
- `README.md` - (this file) quick usage steps

Quick usage (on an EC2 with Docker, k3s, istioctl, helm installed):
  1. Build and push images (replace DOCKERHUB_USER):
     - NodeJS:
       docker build -t DOCKERHUB_USER/demo-canary:v1 app/nodejs
       docker push DOCKERHUB_USER/demo-canary:v1
       docker build -t DOCKERHUB_USER/demo-canary:v2 app/nodejs
       docker push DOCKERHUB_USER/demo-canary:v2
     - Python (optional):
       docker build -t DOCKERHUB_USER/demo-canary-py:v1 app/python
       docker push DOCKERHUB_USER/demo-canary-py:v1
       docker build -t DOCKERHUB_USER/demo-canary-py:v2 app/python
       docker push DOCKERHUB_USER/demo-canary-py:v2
  2. Deploy Helm chart (set image repo via --set or edit values.yaml):
     helm upgrade --install demo-canary chart/demo-canary --namespace canary-demo --create-namespace --set image.repository=DOCKERHUB_USER/demo-canary
  3. Verify traffic split via istio ingress (kubectl -n istio-system get svc istio-ingressgateway) and curl the EXTERNAL-IP.
  4. Change traffic weights with helm upgrade --set stable.weight=50 --set canary.weight=50
  5. Rollback by setting stable.weight=100 --set canary.weight=0 or scaling canary to 0.

See `strategy.md` for canary strategy, metrics to watch, and rollback criteria.
