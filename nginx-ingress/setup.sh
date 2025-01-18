kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.3.0/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.16.2/cert-manager.yaml

Kubectl apply -f clusterissuer.yaml
Kubectl apply -f deploy-one.yaml
Kubectl apply -f deploy-two.yaml
Kubectl apply -f ingress.yaml
