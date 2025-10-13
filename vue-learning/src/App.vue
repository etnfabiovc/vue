<template>
  <div class="layout">
    <!-- Header fixo -->
    <header class="header">
      <h1>Gestor Vue</h1>
      <nav>
        <RouterLink to="/">🏠 Início</RouterLink>
        <RouterLink to="/tasks">📝 Tasks</RouterLink>
        <RouterLink to="/counter">📝 Contador</RouterLink>
      </nav>
    </header>

    <!-- Corpo dividido entre sidebar e conteúdo -->
    <div class="body">
      <aside class="sidebar">
        <ul>
          <li><RouterLink to="/">Dashboard</RouterLink></li>
          <li><RouterLink to="/tasks">Tasks</RouterLink></li>
          <li><RouterLink to="/counter">Contador</RouterLink></li>
          <li><a href="#">Configurações</a></li>
        </ul>
      </aside>

      <main class="content">
        <RouterView /> <!-- muda conforme a rota -->
      </main>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* HEADER */
.header {
  background-color: #42b883;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
}
.header nav a {
  color: white;
  margin-left: 15px;
  text-decoration: none;
}
.header nav a.router-link-exact-active {
  text-decoration: underline;
}

/* CORPO PRINCIPAL */
.body {
  display: flex;
  flex: 1;
}

/* SIDEBAR */
.sidebar {
  width: 200px;
  background: #35495e;
  color: white;
  padding: 20px;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  margin-bottom: 15px;
}
.sidebar a {
  color: white;
  text-decoration: none;
}
.sidebar a.router-link-exact-active {
  font-weight: bold;
  color: #42b883;
}

/* CONTEÚDO */
.content {
  flex: 1;
  padding: 20px;
  background: #f8f8f8;
  overflow-y: auto;
}
</style>
