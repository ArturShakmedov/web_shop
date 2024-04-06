<script>
import axios from "axios";

export default {
  name: "HelloWorld",
  data() {
    return {
      collections: [],
    };
  },
  mounted() {
    this.fetchCollections();
  },
  methods: {
    fetchCollections() {
      axios
        .get("http://127.0.0.1:8000/collections/")
        .then((response) => {
          this.collections = response.data;
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
    <h2>Категории</h2>
    <ul>
      <li v-for="collection in collections" :key="collection.id">
        <a class="collection-item" href="">
          {{ collection.title }} - ({{ collection.products_count }})
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
li {
  list-style-type: none;
}

.collection-item {
  text-decoration: none;
  color: black;
}
</style>
