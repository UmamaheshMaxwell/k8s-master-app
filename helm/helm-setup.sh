#!/bin/bash

###############################################
#          🌐 Setup Nginx Ingress Controller 
###############################################

# 📦 Add the ingress-nginx Helm repository
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx

# 🔄 Update Helm repositories
helm repo update

# 🚀 Install Nginx Ingress Controller
helm install ingress-nginx ingress-nginx/ingress-nginx --version 4.11.3 --namespace ingress-nginx --create-namespace

#!/bin/bash

###############################################
#          🔒 Setup Cert-Manager             #
###############################################

# 📦 Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io --force-update

# 🚀 Install Cert-Manager with CRDs enabled
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --version v1.16.2 \
  --set crds.enabled=true

# ✅ Cert-Manager installation complete

 