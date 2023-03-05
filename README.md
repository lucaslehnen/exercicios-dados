# IGTI Dados Cloud

Repositório para arquivar anotações de revisão do básico de Kubernetes e Airflow vistos no bootcamp do IGTI

## Criando pods de maneira imperativa

    kubectl  get nodes
    kubectl run nginx --image=nginx --port=80
    kubectl get pods
    watch kubectl get pods
    kubectl describe pod nginx
    kubectl port-forward pod/nginx 8080:80
    kubectl delete pod nginx

## Criando pods de maneira declarativa

Criei o manifesto na pasta manifests e rodei o comando para aplicar:

    kubectl apply -f manifests/pod.yaml

Acompanhar status dos pods: (parecido com o watch)

    kubectl get pods -w

Fiz um exemplo com dois containers dentro do Pod:
    kubectl apply -f manifests/pod_dois_containers.yaml
    kubectl describe pod nginx-redis
    kubectl port-forward pod/nginx-redis 6379:6379
    kubectl port-forward pod/nginx-redis 8080:80

Acompanhar logs dos containers:

    kubectl logs pods/nginx-redis
    kubectl logs pods/nginx-redis -c redis -f

## Services

- ClusterIP: Diferentes pods dentro do cluster
- NodePort: IP Interno que permite acesso externo
- LoadBalancer:
- ExternalName: Mapeia um serviço interno para um nome de DNS

    kubectl apply -f manifests/service.yaml
    kubectl get svc -n site
    kubectl port-forward svc/nginx -n site 8080:80
    kubectl get all -n site
    kubectl delete -f manifests/service.yaml

O K3s usa o ServiceLB, mas por padrão ele não adiciona os labels necessários para o funcionamento: https://docs.k3s.io/networking#controlling-servicelb-node-selection

Adicionei os labels no nó para conseguir simular um LoadBalancer:

    kubectl label nodes k3s-11s svccontroller.k3s.cattle.io/enablelb=true

Depois que fiz isso, o Kubernetes atribui o ip externo do service, mas não consegui fazer funcionar.
Vou testar o metallb no lugar assim que precisar no futuro.

    kubectl apply -f manifests/service_k3s.yaml

## ConfigMaps e Secrets

Pegar o arquivo de exemplo dentro do container em `/etc/nginx/conf.d/default.conf`:

    kubectl apply -f manifests/pod.yaml
    kubectl exec -it pod/nginx -- bash
    kubectl delete -f manifests/pod.yaml

Usei para montar o `configmap.yaml`

    kubectl get pods -n site
    kubectl apply -f manifests/configmap.yaml
    kubectl port-forward pod/nginx -n site 8000:8000

Criando a secret de forma imperativa:

    kubectl create secret generic aws-credentials --from-literal=AWS_ACCESS_KEY_ID=<> --from-literal=AWS_SECRET_ACCESS_KEY=<>

## Deployment e replicaset

    kubectl apply -f manifests/replicaset.yaml
    kubectl get pods -n site
    kubectl apply -f manifests/deployments.yaml
    kubectl get all -n site
    kubectl rollout status deployment/nginx -n site
    kubectl rollout history deployment/nginx -n site
    kubectl annotate deployment/nginx kubernetes.io/change-cause="teste 2" -n site
    kubectl rollout undo deployment/nginx -n site

## Storage Class e Volumes claim

    kubectl get sc
    kubectl apply -f manifests/pv.yaml
    kubectl get pvc
    kubectl get pv
    kubectl get pods
    kubectl exec -it pod/nginx -- bash
    kubectl port-forward pod/nginx 8080:80
    kubectl delete pod nginx
    kubectl apply -f manifests/pv.yaml
    kubectl port-forward pod/nginx 8080:80

Demorou um pouco, mas criou o volume e ficou como Bound


## Statefullset


## Helm chart

    sudo apt-get install helm
    curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
    sudo apt-get install apt-transport-https --yes
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
    sudo apt update
    sudo apt-get install helm
    cd helmcharts/
    helm create mychart
    helm install myrelease ./mychart/
    export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=mychart,app.kubernetes.io/instance=myrelease" -o jsonpath="{.items[0].metadata.name}")
    helm status myrelease
    helm uninstall myrelease
    helm install myrelease ./mychart/ -f custom.yaml
    helm uninstall myrelease