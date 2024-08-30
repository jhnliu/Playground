import streamlit as st
import requests
import pandas as pd

def get_district(address):
  url = f"https://www.als.gov.hk/lookup?q={address}"
  response = requests.get(url, headers={"Accept": "application/json"})
  result = response.json()
  result = result['SuggestedAddress'][0]
  print(result)
  return result

def main():
  st.title("Address District Extractor")

  tab1, tab2 = st.tabs(["Bulk Address Extraction", "Single Address Extraction"])

  # File uploader
  with tab1:

    uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])

    if uploaded_file is not None:
        if uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        if 'office_address' in df.columns:
            progress_bar = st.progress(0)
            total_addresses = len(df)

            districts, scores = [], []
            for i, address in enumerate(df['office_address']):
                result = get_district(address)
                district = result['Address']['PremisesAddress']['EngPremisesAddress']['EngDistrict']['DcDistrict']
                score = result['ValidationInformation']['Score']

                districts.append(district)
                scores.append(score)
                progress_bar.progress((i + 1) / total_addresses)

            df['District'] = districts
            df['Confidence Score'] = scores
            st.dataframe(df)  # Display the updated table
        else:
            st.error("The uploaded file does not contain a column named 'office_address'.")


  with tab2:
    address = st.text_input("Enter an address:")


    if st.button("Get District"):
      result = get_district(address)

      st.subheader("English Premises Address")
      eng_address = result['Address']['PremisesAddress']['EngPremisesAddress']
      st.text_input("District", eng_address['EngDistrict']['DcDistrict'])
      st.text_input("Region", eng_address['Region'])

      st.subheader("Chinese Premises Address")
      chi_address = result['Address']['PremisesAddress']['ChiPremisesAddress']
      st.text_input("District", chi_address['ChiDistrict']['DcDistrict'])
      st.text_input("Region", chi_address['Region'])


if __name__ == "__main__":
  main()