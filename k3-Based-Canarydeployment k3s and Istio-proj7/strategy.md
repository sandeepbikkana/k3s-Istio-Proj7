# Canary Deployment Strategy Document

**Objective:** Reduce risk by gradually shifting production traffic from a stable release (v1)
to a new release (v2) while monitoring errors, latency, and business metrics.

## Environment
- K3s single/multi-node cluster
- Istio service mesh for traffic splitting
- Helm for reproducible deployments
- Prometheus/Grafana/Kiali (included in Istio demo profile) for observability

## Steps
1. **Build & Deploy Canary**
   - Deploy v2 alongside v1 with small replica count (1 pod).
   - Route a small percentage of traffic (e.g., 5-20%) to the canary using Istio VirtualService.
2. **Observe (5–30 minutes)**
   - Error rate (5xx) should remain within baseline (e.g., <1% increase).
   - Latency (p95) should not exceed baseline by more than 20%.
   - No increase in pod restarts, OOMs, or CPU/Memory throttling for canary pods.
   - Key business metrics (conversion, throughput) stable.
3. **Progressive Ramp**
   - Increase traffic in steps: 5% -> 20% -> 50% -> 100% as confidence grows.
   - At each step wait enough to collect meaningful data (minutes depending on traffic volume).
4. **Promote or Rollback**
   - If healthy, promote to 100% and scale down/remove v1.
   - If unhealthy, immediately rollback to 100% v1 and investigate.

## Metrics & Alerts (examples)
- Increase alert if 5xx > 1% sustained for 3 minutes.
- Alert if p95 latency > 2x baseline for 3 minutes.
- Alert on pod restarts (> 1 restart in 5 minutes).

## Automation ideas
- Use Prometheus alertmanager to trigger an automated rollback script that patches the VirtualService.
- Use a GitOps tool (ArgoCD/Flux) to version and apply VirtualService changes controlled by CI pipelines.

