<script>
  import MultiSelect from "svelte-multiselect";
  import Plot from "svelte-plotly.js";
  import * as math from "mathjs";

  let { data } = $props();

  let grouping = $state("stage");
  let geneData = $state({});
  let selected = $state([]);

  const CATEGORIES = ["metestrus", "proestrus", "estrus", "male"];
  const GENES = data.availableGenes;

  /// Retrieves the data for a gene. Data has the following form:
  ///{
  ///  "measurements": [
  ///      {
  ///          "sample_id": "Sample_8-CTX_216_361",
  ///          "gene_name": "Narf",
  ///          "ensembl_id": "ENSMUSG00000000056.8",
  ///          "stage": "metestrus",
  ///          "rpkm": 10.03
  ///      },
  ///      ...
  ///  ]
  ///}
  const getGene = async (geneName) => {
    const res = await fetch(`/gonadal/gene?gene=${geneName}`);
    const data = (await res.json()).measurements;
    geneData[geneName] = data;
  };

  const removeGene = async (geneName) => {
    delete geneData[geneName];
  };

  const formatGene = (geneName, geneData) => {
    const grouped = Object.groupBy(geneData, (x) => x.stage);
    const metestrus = {
      mean: math.mean(grouped.metestrus.map((x) => x.rpkm)),
      std:
        math.std(grouped.metestrus.map((x) => x.rpkm)) /
        math.sqrt(grouped.metestrus.length),
    };
    const estrus = {
      mean: math.mean(grouped.estrus.map((x) => x.rpkm)),
      std:
        math.std(grouped.estrus.map((x) => x.rpkm)) /
        math.sqrt(grouped.estrus.length),
    };
    const proestrus = {
      mean: math.mean(grouped.proestrus.map((x) => x.rpkm)),
      std:
        math.std(grouped.proestrus.map((x) => x.rpkm)) /
        math.sqrt(grouped.proestrus.length),
    };
    const male = {
      mean: math.mean(grouped.male.map((x) => x.rpkm)),
      std:
        math.std(grouped.male.map((x) => x.rpkm)) /
        math.sqrt(grouped.male.length),
    };

    return {
      name: geneName,
      x: CATEGORIES,
      y: [metestrus.mean, proestrus.mean, estrus.mean, male.mean],
      type: "bar",
      error_y: {
        type: "data",
        array: [metestrus.std, proestrus.std, estrus.std, male.std],
        visible: true,
      },
    };
  };

  const formatByGene = (rawData) => {
    const data = Object.values(rawData).flat(Infinity);
    let formattedData = [];

    CATEGORIES.forEach((stage) => {
      const stageData = data.filter((x) => x.stage === stage);
      const grouped = Object.groupBy(stageData, (x) => x.gene_name);
      const averages = Object.entries(grouped).map((x) =>
        math.mean(x[1].map((x) => x.rpkm)),
      );
      const stds = Object.entries(grouped).map((x) =>
        math.std(x[1].map((x) => x.rpkm)),
      );

      formattedData.push({
        name: stage,
        x: Object.keys(grouped),
        y: averages,
        type: "bar",
        error_y: {
          type: "data",
          array: stds,
          visible: true,
        },
      });
    });

    return formattedData;
  };
</script>

<h2>TRAPSeq expression data along the female mouse estrous cycle</h2>

<p class="text-center mt-[20px] font-bold">
  Select the gene(s) for which you wish to retrieve the TRAPSeq data:
</p>

<MultiSelect
  bind:selected
  options={GENES}
  placeholder="Select genes"
  maxOptions={10}
  onadd={(x) => getGene(x.option)}
  onremove={(x) => removeGene(x.option)}
  --sms-bg="white"
/>
<div class="text-[0.7em] text-center">
  The Ensembl ID is appended to the gene name if multiple splicing variants are
  present in the database.
</div>

<p class="text-center mt-[20px] font-bold">Group bars by:</p>

<div class="flex flex-row justify-center mb-[20px]">
  <div class="mx-[10px]">
    <input
      type="radio"
      id="contactChoice2"
      name="stage"
      value="stage"
      bind:group={grouping}
    />
    <label for="contactChoice2">Cycle stage</label>
  </div>
  <div class="mx-[10px]">
    <input
      type="radio"
      id="contactChoice3"
      name="gene"
      value="gene"
      bind:group={grouping}
    />
    <label for="contactChoice3">Gene</label>
  </div>
</div>

<Plot
  data={grouping === "stage"
    ? Object.entries(geneData).map((g) => formatGene(g[0], g[1]))
    : formatByGene(geneData)}
  layout={{
    height: 350,
    margin: { t: 0 },
    paper_bgcolor: "rgba(0,0,0,0)", // Sets the background color of the entire plot area (including margins) to transparent
    plot_bgcolor: "rgba(0,0,0,0)", // Sets the background color of the plotting area itself to transparent
  }}
  fillParent="width"
  debounce={250}
/>

<div class="flex flex-row justify-center">
  <a href={`/gonadal/gene/download?query=${selected.join(",")}`} download>
    <button
      disabled={selected.length === 0}
      class={`w-[200px] ${selected.length === 0 ? "bg-gray-500 opacity-40" : "bg-blue-500 hover:bg-blue-700"} text-white font-bold py-2 px-4 rounded mx-auto`}
      onclick={downloadCsv}
    >
      Download as CSV
    </button>
  </a>
</div>
