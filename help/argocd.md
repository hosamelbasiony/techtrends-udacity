kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl get svc -n argocd argocd-server -o yaml > argocd-nodeport.yaml
<!-- 
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:    app.kubernetes.io/component: server    app.kubernetes.io/name: argocd-server
    app.kubernetes.io/part-of: argocd
  name: argocd-server-nodeport
  namespace: argocd
spec: 
  ports:
  - name: http
    port: 80
    protocol: TCP
    targetPort: 8080
    nodePort: 30007
  - name: https
    port: 443
    protocol: TCP
    targetPort: 8080
    nodePort: 30008
  selector:
    app.kubernetes.io/name: argocd-server
  sessionAffinity: None
  type: NodePort 
status:
  loadBalancer: {} 
-->

kubectl apply -f argocd-nodeport.yaml
kubectl get svc -n argocd 

https://192.168.50.4:30008
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
=> admin
=> password HodZatL2YNvHBk0-

https://github.com/kgamanji/argocd-demo/blob/main/python-manifests/deployment.yaml

# to create application crd
kubectl apply -f argocd-python.yaml
kubectl apply -f argocd-hosam-udacity.yaml
kubectl get application -n argocd -o wide

kubectl get po -A
kubectl get po -n argocd 