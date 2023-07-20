import { SECRET_OPENAI_API_KEY } from '$env/static/private';
import { Configuration, OpenAIApi, type ChatCompletionRequestMessage } from 'openai';

const configuration = new Configuration({
	apiKey: SECRET_OPENAI_API_KEY
});
const openai = new OpenAIApi(configuration);

export async function createChatCompletion(
	document: string[],
	question: string,
	knowledge: string[]
): Promise<string | null> {
	let messages = [];
	let systemContent = `You are an assistant designed to help in the elaboration of bids. You are an expert in traffic, ITS and toll systems. 
	You will be provided with informacion regarding tender requirements. 
	The following information is from tender documents:`;

	systemContent += '\n\n```';
	for (let i = 0; i < document.length; i++) {
		systemContent += '\n' + document[i];
	}

	systemContent +=
	'\n```\n\nNow, I provide you information from past proposals from our company that you can use to provide a better answer:';

	systemContent += '\n\n```';
	for (let i = 0; i < knowledge.length; i++) {
		systemContent += '\n' + knowledge[i];
	}

	systemContent +=
		'\n```\n\nThe user will ask you to provide a proposal that fits tender requirements. You can use info from past proposals.';

	messages.push({
		role: 'system',
		content: systemContent
	} satisfies ChatCompletionRequestMessage);

	let prompt = question;

	messages.push({
		role: 'user',
		content: prompt
	} satisfies ChatCompletionRequestMessage);

	//console.log(messages);
	try {
		let response = await openai.createChatCompletion({
			model: 'gpt-3.5-turbo',
			messages: messages,
			temperature: 1,
			max_tokens: 1000
		});

		if (response.data.choices.length > 0) {
			return response.data.choices[0].message!.content;
		} else {
			return null;
		}
	} catch (error: any) {
		if (error.response) {
			console.log(error.response.status);
			console.log(error.response.data);
		} else {
			console.log(error.message);
		}
		return null;
	}
}
