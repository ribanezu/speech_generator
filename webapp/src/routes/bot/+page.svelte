<script lang="ts">
	import { PUBLIC_PROCESS_FILES_SERVER } from '$env/static/public';
	import { CodeBlock, ProgressBar } from '@skeletonlabs/skeleton';
	import { construct_svelte_component } from 'svelte/internal';
	let query = '';
	let documents: string[] = [];
	let metadatas: MetaData[] = [];
	let knowledge: string[] = [];
	let metadata_knowledge: MetaData[] = [];
	let parsedTextBlocks: TextBlock[] = [];
	let loading = false;

	interface QueryResult {
		documents: string[][];
		distances: number[][];
		metadatas: MetaData[][];
	}


	interface MetaData {
		document_title: string;
		file_name: string;
	}

	async function queryEmbeddings() {
		loading = true;
		const response = await fetch(`${PUBLIC_PROCESS_FILES_SERVER}/query?text=${query}`, {
			method: 'GET'
		});
		let result: QueryResult = await response.json();
		documents = result.documents[0];
		metadatas = result.metadatas[0];

		const response2 = await fetch(`${PUBLIC_PROCESS_FILES_SERVER}/query_knowledge?text=${query}`, {
			method: 'GET'
		});
		let result2: QueryResult = await response2.json();
		knowledge = result2.documents[0];
		metadata_knowledge = result2.metadatas[0];
		await queryLLM();
	}

	async function queryLLM() {
		const response = await fetch('/query_bot', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query: query,
				documents: documents,
				knowledge: knowledge
			})
		});
		//console.log(response.body);
		let result = await response.json();
		parsedTextBlocks = parseText(result.answer);
		loading = false;
	}

	interface TextBlock {
		isCodeBlock: boolean;
		text: string;
		language?: string;
	}

	function parseText(text: string): TextBlock[] {
		const regex = /```([\w-]+)?\s*([\s\S]+?)\s*```/g;
		const blocks: TextBlock[] = [];
		let lastIndex = 0;
		let match;

		while ((match = regex.exec(text))) {
			const [fullMatch, language, code] = match;
			const preMatch = text.slice(lastIndex, match.index);
			if (preMatch) {
				blocks.push({ isCodeBlock: false, text: preMatch });
			}
			blocks.push({ isCodeBlock: true, text: code, language });
			lastIndex = match.index + fullMatch.length;
		}

		const lastBlock = text.slice(lastIndex);
		if (lastBlock) {
			blocks.push({ isCodeBlock: false, text: lastBlock });
		}

		return blocks;
	}
</script>

<div class="flex justify-center items-center p-4">
	<div class="m-11 card h-full w-3/4">
		<div class="p-4 md:p-10">
			<h1><img src="/indra_logo.png" alt="logo" style="height: 100px; vertical-align: middle;"> Mobility Ofertas</h1>
			<br />
			<h3 class="mb-3">Indicado para pedir extractos para ofertas en inglés.</h3>
			<p class="text-xl mb-2">Pregunta lo que quieras:</p>
			<div class="flex">
				<input
					class="input text-xl"
					type="text"
					placeholder="qué te interesa saber..."
					bind:value={query}
				/>
				<button
					type="button"
					class="btn variant-filled-secondary w-1/5 ml-4 text-xl"
					on:click={queryEmbeddings}>Ask</button
				>
			</div>

			{#if loading}
				<div class="p-8">
					Searching...<br />
					<ProgressBar height="h-3" meter="bg-warning-500" />
				</div>
			{:else}
				{#if parsedTextBlocks.length > 0}
					<div>
						<h3 class="text-xxl mb-2 mt-6">Respuesta:</h3>
						<div class="flex flex-col rounded-[16px] bg-gray-700 p-4">
							{#each parsedTextBlocks as textBlock}
								{#if textBlock.isCodeBlock}
									<CodeBlock language={textBlock.language} code={textBlock.text} />
								{:else}
									<p style="white-space: pre-line;">{textBlock.text}</p>
								{/if}
							{/each}
						</div>
					</div>
				{/if}
				<div>
					{#if documents.length > 0}
						<p class="text-xl mb-2 mt-6">Pliegos:</p>
						{#each documents as document, i}
							<div class="flex flex-col">
								<CodeBlock language="markdown" code={document} />
								<p class="mt-2">Archivo origen: {metadatas[i].file_name}</p>
							</div>
							<br />
						{/each}
					{/if}
				</div>
				<div>
					{#if knowledge.length > 0}
						<p class="text-xl mb-2 mt-6">Ofertas anteriores:</p>
						{#each knowledge as document, i}
							<div class="flex flex-col">
								<CodeBlock language="markdown" code={document} />
								<p class="mt-2">Archivo origen: {metadata_knowledge[i].file_name}</p>
							</div>
							<br />
						{/each}
					{/if}
				</div>
			{/if}
		</div>
	</div>
</div>
