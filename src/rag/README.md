\# RAG



Finds relevant paper chunks and builds a grounded prompt for the LLM.



\## Files

\- retriever.py: retrieve(query, k=5, filters=None) returns RetrievedChunk dicts

\- prompt\_builder.py: build\_rag\_prompt(question, chunks)

\- demo.py: shows ingestion, search and the RAG prompt end to end

\- test\_queries.py: runs 10 sample queries to check relevance by hand



\## Use

from retriever import retrieve

chunks = retrieve("your question", k=5, filters={"peer\_reviewed": True})



\## Notes

\- Chunks come from the Milvus Lite DB built by src/ingestion/build\_index.py

\- filters={"peer\_reviewed": True} returns peer-reviewed papers only

\- The prompt tells the LLM to use only the context and to cite chunk ids

\- Calling an LLM is done by the orchestrator (Module 1), not here

