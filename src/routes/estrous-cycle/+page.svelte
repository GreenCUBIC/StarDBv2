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
    const res = await fetch(`/estrous-cycle/gene?gene=${geneName}`);
    const data = (await res.json()).measurements;
    geneData[geneName] = data;
  };

  const removeGene = async (geneName) => {
    delete geneData[geneName];
  };

  const formatGene = (geneName, data) => {
    const estrus = data.filter((x) => x.stage === "estrus")[0];
    const metestrus = data.filter((x) => x.stage === "metestrus")[0];
    const male = data.filter((x) => x.stage === "male")[0];
    const proestrus = data.filter((x) => x.stage === "proestrus")[0];

    return {
      name: geneName,
      x: CATEGORIES,
      y: [metestrus.mean, proestrus.mean, estrus.mean, male.mean],
      type: "bar",
      error_y: {
        type: "data",
        array: [metestrus.error, proestrus.error, estrus.error, male.error],
        visible: true,
      },
    };
  };

  const formatByGene = (data) => {
    let traces = [];

    CATEGORIES.forEach((stage) => {
      let stageData = [];
      Object.entries(data).forEach((x) => stageData.push(x[1].filter((g) => g.stage === stage)[0]));

      traces.push({
        name: stage,
        x: stageData.map((x) => x.gene_name), // genes
        y: stageData.map((x) => x.mean), // averages
        type: "bar",
        error_y: {
          type: "data",
          array: stageData.map((x) => x.error), // stds for stage
          visible: true,
        },
      });
    });

    return traces;
  };
</script>

<h2>TRAPSeq expression data along the female mouse estrous cycle</h2>

<p class="text-center mt-[20px] font-bold"> Select the gene(s) for which you wish to retrieve the TRAPSeq data: </p>

<MultiSelect bind:selected options={GENES} placeholder="Select genes" maxOptions={10} onadd={(x) => getGene(x.option)} onremove={(x) => removeGene(x.option)} --sms-bg="white" />
<div class="text-[0.7em] text-center"> The Ensembl ID is appended to the gene name if multiple splicing variants are present in the database. </div>

<p class="text-center mt-[20px] font-bold">Group bars by:</p>

<div class="flex flex-row justify-center mb-[20px]">
  <div class="mx-[10px]">
    <input type="radio" id="contactChoice2" name="stage" value="stage" bind:group={grouping} />
    <label for="contactChoice2">Cycle stage</label>
  </div>
  <div class="mx-[10px]">
    <input type="radio" id="contactChoice3" name="gene" value="gene" bind:group={grouping} />
    <label for="contactChoice3">Gene</label>
  </div>
</div>

<Plot
  data={grouping === "stage" ? Object.entries(geneData).map((g) => formatGene(g[0], g[1])) : formatByGene(geneData)}
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
  <a href={`/estrous-cycle/gene/download?query=${selected.join(",")}`} download>
    <button disabled={selected.length === 0} class={`w-[200px] ${selected.length === 0 ? "bg-gray-500 opacity-40" : "bg-blue-500 hover:bg-blue-700"} text-white font-bold py-2 px-4 rounded mx-auto`}>
      Download as CSV
    </button>
  </a>
</div>
