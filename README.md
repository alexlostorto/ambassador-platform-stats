<h1 align="center">Ambassador Platform Stats</h1>

<p align="center">
  <b>Display 'The Ambassador Platform' message statistics.</b>
</p>

[![Maintainability](https://img.shields.io/codeclimate/maintainability/alexlostorto/ambassador-platform-stats?style=for-the-badge&message=Code+Climate&labelColor=222222&logo=Code+Climate&logoColor=FFFFFF)](https://codeclimate.com/github/alexlostorto/ambassador-platform-stats/maintainability)

The program contacts **The Ambassador Platform's API** and then outputs the statistics for your chats.

_Note: [The Ambassador Platform](https://www.theambassadorplatform.com/) is a chat system used by institutions to let student ambassadors talk to prospective students._

```python
# Example in console
Alex: 5,672
Jane: 6,673
Times Alex said '😎':  4
Times Jane said '😎':  9
Total messages: 12,345
Total times '😎' was said:  13
```

## ⚡ Quick setup

1. Clone the repo

```bash
git clone https://github.com/alexlostorto/ambassador-platform-stats
```

2. Rename _.env.example_ to _.env_

3. Replace the _token_ with the **JWT Token** made in the network request, and replace _dialog_ with your ambassador's **dialog ID**.

```env
TOKEN=eyJhb...
DIALOG=123456
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run main.py

```bash
python main.py
```

6. Star the repo 😄

## 📜 Credits

Everything is coded by Alex lo Storto

Licensed under the MIT License.
