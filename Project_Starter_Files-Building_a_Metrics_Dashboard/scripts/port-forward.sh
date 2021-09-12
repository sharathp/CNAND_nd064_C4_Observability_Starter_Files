# kill all kubectl processes, assuming all these processes are port-forwards
kill $(ps aux | grep 'kubectl' | awk '{print $2}')

kubectl port-forward service/prometheus-grafana --address 0.0.0.0 3000:80 -n monitoring &
kubectl port-forward service/prometheus-kube-prometheus-prometheus --address 0.0.0.0 9090:9090 -n monitoring &
kubectl port-forward service/nd064course4-query --address 0.0.0.0 16686:16686 -n observability &
kubectl port-forward service/frontend --address 0.0.0.0 8080:8082 &
kubectl port-forward service/trial --address 0.0.0.0 8083:8083 &
kubectl port-forward service/backend --address 0.0.0.0 8081:8081 &
