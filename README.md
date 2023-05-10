# android-ransomware-detection
Android ransomware detection using the negative selection algorithm and syscall frequencies.

## Train the model
1. Training based on static features (permissions):
```
python main.py static train
```
2. Training based on dynamic features (system calls):
```
python main.py dynamic train
```

## Test the model
1. Test static results:
```
python main.py static classify
```
2. Test dynamic results:
```
python main.py dynamic classify
```

## Notes
* Data, such as applications and system call logs, are not provided.
