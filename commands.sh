az webapp up --sku F1 -n <app-name>
az group create --location eastus --name <rg-group-name> 
az group delete -n <rg-group-name> 
az vm create -n myVM -g <rg-group-name> --image UnuntuLTS --generate ssh-key-gen-keys
az account list 
azure cloud console ssh-keygen -t rsa