<script lang="ts">
  import favicon from "$lib/assets/favicon.svg";
  import Logo from "$lib/logo.svelte";
  import "../app.css";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
</svelte:head>

<main class="box">
  <div class="flex flex-row justify-center">
    <a href="/">
      <Logo />
    </a>
  </div>
  {@render children?.()}

  <footer id="footer" class="text-center">
    <hr id="foot-rule" />
    <div class="font-bold text-center my-[10px]">
      If you used our database, please cite the appropriate paper (<a download href="/rurakdevelopment.bib">Development</a>
      or <a download href="/rurakestrouscycle.bib">Estrous cycle</a>).
    </div>
    <div>
      For technical details regarding the work, please contact <a href="mailto:natalinasalmaso@cunet.carleton.ca">Dr. Natalina Salmaso</a>.
    </div>
    <div>
      To report a bug or a feature request, please contact <a href="mailto:francois@charih.ca">François Charih</a>
    </div>
    <img id="carleton-logo" src="/img/carletonblack-01.svg" />
    <div>
      Online database built by <a href="https://charih.ca">François Charih</a>
    </div>
    <div>{"© Salmaso Lab, " + new Date().getFullYear()}</div>
  </footer>
</main>

<style>
  .box {
    width: 80%;
    background: rgb(209, 209, 209, 0.95);
    border: 3px solid black;
    margin: 0 auto;
    padding: 20px;
  }

  #carleton-logo {
    display: block;
    margin: 10px auto;
    width: 20%;
  }

  #foot-rule {
    width: 80%;
    border: 0.5px solid black;
  }

  #footer {
    margin-top: 20px;
  }

  .logo-container {
    display: flex;
    justify-content: center;
  }
</style>
