from app import app

if __name__ == '__main__':
    app.run(debug=True)
else:
    # 这是为 Vercel 准备的
    application = app 