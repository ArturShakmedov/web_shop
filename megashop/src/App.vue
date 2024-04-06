<script setup>
import HelloWorld from "./components/HelloWorld.vue";
import TheWelcome from "./components/TheWelcome.vue";
</script>

<template>
  <div class="container">
    <div class="left">
      <HelloWorld />
    </div>
    <div class="right">
      <TheWelcome />
    </div>
  </div>
</template>

<style scoped>
.container {
  width: 1200px;
  padding: 20px;
  border-radius: 20px;
  background-color: antiquewhite;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.left {
  width: calc(30% - 10px);
  text-align: center;
  padding: 10px;
  margin: 10px;
  background-color: antiquewhite;
  color: black;
}
.right {
  width: calc(70% - 10px);
  text-align: center;
  padding: 10px;
  margin: 10px;
  background-color: antiquewhite;
  color: black;
}
</style>
