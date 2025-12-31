import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [webApp, setWebApp] = useState(null)

  useEffect(() => {
    // Инициализация Telegram WebApp
    const tg = window.Telegram?.WebApp
    if (tg) {
      tg.ready()
      setWebApp(tg)
    }
  }, [])

  return (
    <div className="app">
      <header className="header">
        <h1>TgWork</h1>
        <p>Фриланс-биржа в Telegram</p>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Добро пожаловать!</h2>
          <p>Это MVP версия TgWork. Вскоре здесь появятся услуги, заказы и чат.</p>
          
          {webApp && (
            <div className="user-info">
              <p>User ID: {webApp.initDataUnsafe?.user?.id}</p>
            </div>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
