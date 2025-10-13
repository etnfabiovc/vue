<script setup lang="ts">

</script>

<template>
    <div class="header">
        <div class="title-container">
            <h1>Sistema de Solicitações e Serviços</h1>
            <p>DEPARTAMENTO DE SAÚDE, SEGURANÇA E BEM-ESTAR NO TRABALHO - DSS.A</p>
        </div>
    </div>
</template>

<style scoped>
    .header {
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .title-container {
        display: flex;
        flex-direction: column;
        height: 80px;
        width: 100vw;
        background-color: white;
        box-shadow: 5px 2px rgba(0, 0, 0, 0.04);
        gap: 0;
        padding: 10px;
    }

    h1 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    }

    p {
        font-size: 0.75rem;
        margin: 0;
        font-weight: 500;
        color: rgba(0, 0, 0, 0.5);
    }
</style>