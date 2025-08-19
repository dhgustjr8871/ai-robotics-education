# ai-robotics-education

필요한 Python 패키지 다운로드를 위해 다음 명령어를 터미널에 차례로 입력합니다.

```bash
pip install -r requirements.txt
pip uninstall -y torch torchvision torchaudio
pip cache purge
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
