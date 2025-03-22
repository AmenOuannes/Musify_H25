<template>
  <div class="home">
    <section class="hero">
      <h1>Welcome to Musify</h1>
      <p>Discover new music and playlists.</p>
      <a href="#" class="explore-btn">Explore</a>
    </section>

    <section class="recommended">
      <h2>Recommended for You</h2>
      <div class="playlists">
        <div v-for="playlist in playlists" :key="playlist.id" class="playlist">
          <img :src="playlist.image" :alt="playlist.name" />
          <h3>{{ playlist.name }}</h3>
          <p>{{ playlist.description }}</p>
        </div>
      </div>
    </section>
  </div>

</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      playlists: [
        {
          id: 1,
          name: "Chill Vibes",
          description: "Relaxing tunes for your day.",
          image: "https://via.placeholder.com/150",
        },
        {
          id: 2,
          name: "Workout Mix",
          description: "High-energy tracks to keep you moving.",
          image: "https://via.placeholder.com/150",
        },
        {
          id: 3,
          name: "Top Hits",
          description: "The latest and greatest hits.",
          image: "https://via.placeholder.com/150",
        },
      ],
    };
  },
};
</script>

<style scoped>
.home {
  padding: 20px;
}

.hero {
  text-align: center;
  margin-top: 60px;
}

.hero h1 {
  font-size: 40px;
  margin: 0;
}

.hero p {
  font-size: 20px;
  margin: 10px 0;
}

.explore-btn {
  display: inline-block;
  background: #0f0;
  color: black;
  padding: 14px 28px;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: 0.3s;
  font-size: 18px;
}

.explore-btn:hover {
  background: #0c0;
}

.recommended {
  margin-top: 50px;
}

.recommended h2 {
  font-size: 26px;
  margin-bottom: 20px;
}

.playlists {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.playlist {
  background: #333;
  padding: 15px;
  border-radius: 5px;
  text-align: center;
  transition: 0.3s;
}

.playlist:hover {
  background: #444;
}

.playlist img {
  width: 100%;
  border-radius: 5px;
}
</style>