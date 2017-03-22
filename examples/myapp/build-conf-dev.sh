rm -rf ./logs
mkdir ./logs
confiler ./environments ./src myapp.dev ./packages/dev --log=./logs/dev.log
confiler ./environments ./src myapp.dev.vladik ./packages/dev.vladik --log=./logs/dev.vladik.log
confiler ./environments ./src myapp.dev.staging ./packages/dev.staging --log=./logs/dev.staging.log
