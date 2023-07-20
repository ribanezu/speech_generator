<script lang="ts">
	import { FileDropzone, ProgressBar } from '@skeletonlabs/skeleton';
	import { PUBLIC_PROCESS_FILES_SERVER } from '$env/static/public';
	import { goto } from '$app/navigation';

	let files: FileList;
	let processing = false;
	let error = false;

	function onChangeHandler(e: Event): void {
		files = (e.target as HTMLInputElement).files;
	}

	async function startProcessing(event: Event) {
		processing = true;
		const formEl = event.target as HTMLFormElement;
		const data = new FormData(formEl);
		for (let pair of data.entries()) {
    		console.log(pair[0]+ ', ' + pair[1]); 
		}
		const response = await fetch(`${PUBLIC_PROCESS_FILES_SERVER}/process`, {
			method: 'POST',
			body: data
		});
		let result = await response.json();
		if (result && result.success) {
			goto('/bot');
		} else {
			error = true;
		}
	}

	let otherFiles: FileList;
	let processing2 = false;
	let error2 = false;
	
	function onChangeHandlerOther(e: Event): void {
		otherFiles = (e.target as HTMLInputElement).files;
	}

	async function startProcessingOther(event: Event) {
		processing2 = true;
		const formEl = event.target as HTMLFormElement;
		const data = new FormData(formEl);
		for (let pair of data.entries()) {
    		console.log(pair[0]+ ', ' + pair[1]); 
		}
		const response = await fetch(`${PUBLIC_PROCESS_FILES_SERVER}/process_knowledge`, {
			method: 'POST',
			body: data
		});
		let result = await response.json();
		if (result && result.success) {
			processing2 = false;
		} else {
			error2 = true;
		}
	}






</script>

<div class="flex justify-center items-center p-4">
	<div class="m-11 card h-full w-3/4">
		<div class="p-4 md:p-10">
			<h1><img src="/indra_logo.png" alt="logo" style="height: 100px; vertical-align: middle;"> Mobility Ofertas</h1>
			<h3 class="mt-6">Selecciona los documentos de tu producto:</h3>
			<form method="POST" on:submit|preventDefault={startProcessingOther} class="w-full">
				<div class="flex flex-col justify-center items-center">
					<FileDropzone name="knowledge" multiple bind:otherFiles on:change={onChangeHandlerOther} />
					{#if otherFiles}
						<ol class="list w-full">
							{#each Array.from(otherFiles) as document, i}
								<li>
									<span class="badge-icon p-4 variant-soft-primary">{i + 1}</span>
									<span class="text-xl">{document.name}</span>
								</li>
							{/each}
						</ol>
						<button class="w-2/4 btn variant-filled-secondary btn-lg mt-4" disabled={processing2}
							>Indexar el texto</button
						>
					{/if}
				</div>
			</form>
			{#if processing2}
				<div class="p-8">
					<p>Procesando...</p>
					<ProgressBar height="h-3" meter="bg-warning-500" />
				</div>
			{/if}			
			{#if error2}
				<aside class="alert variant-filled-error">
					<!-- Icon -->
					<div>🚨</div>
					<!-- Message -->
					<div class="alert-message">
						<h3>Error procesando los archivos</h3>
					</div>
				</aside>
			{/if}			
			
			<h3 class="mt-6">Selecciona los documentos del pliego .pdf:</h3>
			<form method="POST" on:submit|preventDefault={startProcessing} class="w-full">
				<div class="flex flex-col justify-center items-center">
					<FileDropzone name="documents" multiple bind:files on:change={onChangeHandler} />
					{#if files}
						<ol class="list w-full">
							{#each Array.from(files) as document, i}
								<li>
									<span class="badge-icon p-4 variant-soft-primary">{i + 1}</span>
									<span class="text-xl">{document.name}</span>
								</li>
							{/each}
						</ol>
						<button class="w-2/4 btn variant-filled-secondary btn-lg mt-4" disabled={processing}
							>Indexar el texto</button
						>
					{/if}
				</div>
			</form>
			{#if processing}
				<div class="p-8">
					<p>Procesando...</p>
					<ProgressBar height="h-3" meter="bg-warning-500" />
				</div>
			{/if}
			{#if error}
				<aside class="alert variant-filled-error">
					<!-- Icon -->
					<div>🚨</div>
					<!-- Message -->
					<div class="alert-message">
						<h3>Error procesando los archivos</h3>
					</div>
				</aside>
			{/if}
		</div>
	</div>
</div>
