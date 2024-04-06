<script>
import axios from "axios";

export default {
  name: "TheWelcome",
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    fetchProducts() {
      axios
        .get("http://127.0.0.1:8000/products/")
        .then((response) => {
          this.products = response.data.results;
        })
        .catch((error) => {
          console.error("Не удалось получить данные", error);
        });
    },
  },
};
</script>

<template>
  <div>
    <h2>Товары</h2>
    <div class="row">
      <div class="card" v-for="product in products" :key="product.id">
        <h3>{{ product.title }}</h3>
        <p>{{ product.price }}$</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  justify-content: center;
}
.card {
  border: 1px solid black;
  border-radius: 10px;
  padding: 20px;
  margin: 20px;
  box-shadow: 10px 5px 5px rgba(0, 0, 0, 0.2);
  width: 200px;
}
</style>