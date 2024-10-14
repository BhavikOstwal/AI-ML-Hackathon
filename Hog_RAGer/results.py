from complete_pipeline import train_data, process_query, json

with open('out/output.json', 'w') as output_file:
  for i in range(len(train_data)):
    test_query = train_data[i]['query']
    output = process_query(test_query)

    # Print output in required format
    # print(json.dumps(output, indent=2))

    # You can now write the results to a JSON file
    json.dump(output, output_file, indent=2)