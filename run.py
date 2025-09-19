import os
from market import app

if __name__ == '__main__':
    #when just run in vscode, not in Render
    #app.run(debug=True)

    #to run in Render
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))





