<script>
  import MultiSelect from "svelte-multiselect";
  import Plot from "svelte-plotly.js";

  let { data } = $props();
  let selected = $state([]);
  let geneData = $state([]);
  let selectedCorrelationGene = $state(null);
  let geneCorrelations = $state({});
  let topGenes = $state(100);
  let sex = $state("both");
  let period = $state("all");

  const getCorrelation = async () => {
    const result = await fetch(`/development/correlation?gene=${selectedCorrelationGene}`);
    geneCorrelations = (await result.json()).correlations;
  };

  const getGene = async (geneName) => {
    const res = await fetch(`/development/gene/query?gene=${geneName}`);
    const data = (await res.json()).measurements;
    geneData = {
      ...geneData,
      [geneName]: data,
    };

    selectedCorrelationGene = geneName;
    getCorrelation();
  };

  const removeGene = async (geneName) => {
    let newData = { ...geneData };
    delete newData[geneName];
    geneData = { ...newData };
  };

  const formatData = (data, period, sex) => {
    let traces = [];
    // If all periods
    if (period === "all") {
      if (sex === "male" || sex === "both") {
        Object.entries(data).forEach((gene) => {
          traces.push({
            name: `${gene[0]} (male)`,
            x: [1, 2, 3, 4, 5, 6],
            y: gene[1].male.map((x) => x.mean_rpkm),
            error_y: {
              type: "data",
              array: gene[1].male.map((x) => x.std_rpkm),
              visible: true,
            },
            type: "line",
          });
        });
      }
      if (sex === "female" || sex === "both") {
        Object.entries(data).forEach((gene) => {
          traces.push({
            name: `${gene[0]} (female)`,
            x: [1, 2, 3, 4, 5, 6],
            y: gene[1].female.map((x) => x.mean_rpkm),
            error_y: {
              type: "data",
              array: gene[1].female.map((x) => x.std_rpkm),
              visible: true,
            },
            type: "line",
          });
        });
      }
      return traces;
    }

    if (sex === "male" || sex === "both") {
      traces.push({
        name: "male",
        x: Object.keys(data),
        y: Object.values(data)
          .map((x) => x.male.filter((x) => x.age === parseInt(period))[0])
          .map((x) => {
            return x.mean_rpkm;
          }),
        type: "bar",
        error_y: {
          type: "data",
          array: Object.values(data)
            .map((x) => x.male.filter((x) => x.age === parseInt(period))[0])
            .map((x) => {
              return x.std_rpkm;
            }),
          visible: true,
        },
      });
    }
    if (sex === "female" || sex === "both") {
      traces.push({
        name: "female",
        x: Object.keys(data),
        y: Object.values(data)
          .map((x) => x.female.filter((x) => x.age === parseInt(period))[0])
          .map((x) => {
            return x.mean_rpkm;
          }),
        type: "bar",
        error_y: {
          type: "data",
          array: Object.values(data)
            .map((x) => x.female.filter((x) => x.age === parseInt(period))[0])
            .map((x) => {
              return x.std_rpkm;
            }),
          visible: true,
        },
      });
    }
    return traces;
  };

  let shownData = $derived.by(() => formatData(geneData, period, sex));
</script>

<h2 class="text-center font-bold">Gene-based query</h2>

<h3>How to use</h3>

<p class="mb-[10px]">
  Select the gene(s) for which you wish to retrieve the translatomic data. You can display the data for male, female or both sexes. You may also consult the data for a specific developmental period by
  selecting the period. Genes whose expression is correlated through development (as assessed by Pearson's <i> r </i>
  statistic) are tabulated. You may click on a row in the table to add this gene to the list of visualized genes.
</p>

<div class="text-center font-bold">Genes</div>
<MultiSelect maxOptions={10} bind:selected options={data.availableGenes} placeholder="Select genes" onadd={(x) => getGene(x.option)} onremove={(x) => removeGene(x.option)} --sms-bg="white" />
<div class="text-[0.7em] font-bold mb-[10px]"> Note: Genes whose translation levels didn't meet a minimum threshold may not appear (see paper for details). </div>

<div class="text-center font-bold">Sex</div>
<fieldset class="text-center">
  <div>
    <input type="radio" id="contactChoice3" name="sex" value="both" bind:group={sex} />
    <label for="contactChoice3">Both</label>
    <input type="radio" id="contactChoice1" name="sex" value="female" bind:group={sex} />
    <label for="contactChoice1">Female</label>

    <input type="radio" id="contactChoice2" name="sex" value="male" bind:group={sex} />
    <label for="contactChoice2">Male</label>
  </div>
</fieldset>

<div class="text-center font-bold mb-[10px]">Development period</div>
<fieldset class="text-center">
  <div>
    <input type="radio" id="contactChoice1" name="period" value="all" bind:group={period} />
    <label for="contactChoice1">All</label>

    <input type="radio" id="contactChoice2" name="period" value="1" bind:group={period} />
    <label for="contactChoice2">P1</label>

    <input type="radio" id="contactChoice3" name="period" value="4" bind:group={period} />
    <label for="contactChoice3">P4</label>

    <input type="radio" id="contactChoice4" name="period" value="7" bind:group={period} />
    <label for="contactChoice4">P7</label>

    <input type="radio" id="contactChoice5" name="period" value="14" bind:group={period} />
    <label for="contactChoice5">P14</label>

    <input type="radio" id="contactChoice6" name="period" value="35" bind:group={period} />
    <label for="contactChoice6">P35</label>

    <input type="radio" id="contactChoice7" name="period" value="100" bind:group={period} />
    <label for="contactChoice7">Adult</label>
  </div>
</fieldset>

<!--<p>
  Show the top <select>
    <option value="100">100</option>
    <option value="500">500</option>
  </select>
  most correlated genes with
</p>-->

<div class="flex flex-row items-center" style="align-items: center;">
  <div style="display: block;">
    {#if period === "all"}
      <div style="width:700px; height:400px;">
        <Plot
          data={shownData}
          fillParent="width"
          debounce={250}
          layout={{
            height: 450,
            margin: { t: 0 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
            xaxis: {
              title: {
                text: "Developmental period",
              },
              tickmode: "array", // Must be 'array' for custom tick values/text
              tickvals: [1, 2, 3, 4, 5, 6],
              ticktext: ["P1", "P4", "P7", "P14", "P35", "Adult"],
            },
            yaxis: {
              title: {
                text: "Translation levels (RPKM)",
              },
              rangemode: "tozero",
            },
          }}
        />
      </div>
    {/if}
    {#if period != "all"}
      <div style="width:700px; height:400px;">
        <Plot
          data={shownData}
          layout={{
            height: 400,
            margin: { t: 0 },
            paper_bgcolor: "rgba(0,0,0,0)",
            plot_bgcolor: "rgba(0,0,0,0)",
          }}
          fillParent="width"
          debounce={250}
        />
      </div>
    {/if}
  </div>
  <div>
    <div class="text-center font-bold mb-[10px]">Correlated genes</div>
    <div class="text-center">
      <!--Show the top
      <select bind:value={topGenes}>
        <option value={100} class="bg-white">100</option>
        <option value={200} class="bg-white">200</option>
        <option value={500} class="bg-blue-500">500</option>
      </select>-->
      500 most correlated genes with
      <select
        bind:value={selectedCorrelationGene}
        onchange={(e) => {
          getCorrelation(e.target.value);
        }}
      >
        {#each Object.keys(geneData) as g}
          <option value={g}>{g}</option>
        {/each}
      </select>
      .
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Gene</th>
              <th>Correlation coefficient</th>
            </tr>
          </thead>
          <tbody>
            {#each geneCorrelations[sex] ? geneCorrelations[sex] : [] as corr}
              <tr
                onclick={() => {
                  getGene(corr.gene_name);
                  selected.push(corr.gene_name);
                }}
              >
                <td>{corr.gene_name}</td>
                <td>{corr.correlation.toFixed(4)}</td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
    <div class="text-[0.7em] text-center">Click on a row to add the gene to the list.</div>
  </div>
</div>
<div class="flex flex-row justify-center mt-[20px]">
  <a href={`/development/download?gene=${selected.join(",")}`} download>
    <button disabled={selected.length === 0} class={`w-[200px] ${selected.length === 0 ? "bg-gray-500 opacity-40" : "bg-blue-500 hover:bg-blue-700"} text-white font-bold py-2 px-4 rounded mx-auto`}>
      Download as CSV
    </button>
  </a>
</div>

<style>
  @reference "tailwindcss";

  #row {
    display: flex;
    justify-content: space-around;
  }

  #settings-area {
    width: 300px;
  }

  .plot-container {
    height: 300px;
    width: 300px;
  }

  div.multiselect {
    background: white;
  }

  .correlations-table {
    width: 100%;
    border: 2px solid black;
  }

  /* Scrollable container */
  .table-container {
    border: 1px solid #e5e7eb;
    border-bottom: none;
    overflow: auto; /* Enables both horizontal and vertical scrolling */
    height: 400px; /* Limits table height for vertical scrolling */
  }

  /* Table layout */
  .table {
    border-collapse: collapse;
    width: 100%;
    table-layout: fixed; /* Ensures consistent column widths */
    border: 2px solid black;
  }

  /* Table cells and headers */
  .table th,
  .table td {
    padding: 8px;
    text-align: center;
    border: 1px solid #e5e7eb;
  }

  /* Frozen first column */
  .table td:nth-child(1) {
    position: sticky;
    left: 0; /* Ensures the column stays on the left */
    z-index: 5; /* Keeps the column above other cells */
    color: black;
  }

  .table th:nth-child(1) {
    position: sticky;
    left: 0; /* Ensures the column stays on the left */
    z-index: 5; /* Keeps the column above other cells */
    color: white;
  }

  /* Add higher z-index for header */
  .table th:nth-child(1) {
    z-index: 6;
  }

  /* Sticky header */
  .table th {
    background-color: black;
    color: white;
    font-size: 14px;
    font-weight: bold;
    position: sticky;
    top: 0; /* Makes the header stick to the top */
    z-index: 2; /* Keeps the header above the table body */
  }

  /* Styling for table body */
  .table td {
    font-size: 14px;
    color: black;
  }

  /* Zebra striping for rows */
  .table tr:nth-child(odd) {
    background-color: #f9fafb;
  }

  /* Hover effect for rows */
  .table tr:hover {
    background-color: rgba(14, 116, 144, 0.1);
  }

  /* No data row styling */
  .no-data {
    text-align: center;
    font-size: 14px;
    color: #9ca3af;
  }
</style>
