import pandas as pd
import numpy as np

def convert_to_cocon_template_old(dataset, streetname, housenumber, suffix, postcode, town):
    output = dataset.copy()
    output['Naam'] = output[postcode].fillna('').astype(str) + ' ' + output[housenumber].fillna('').astype(str) + ' ' + output[suffix].fillna('').astype(str)     
    output['Naam'] = output['Naam'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output['Huisnummer'] = output[housenumber].fillna('').astype(str) + ' ' + output[suffix].fillna('').astype(str)     
    output['Huisnummer'] = output['Huisnummer'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output['Postcode'] = output[postcode].apply(lambda x: ''.join(x.split(' ')) if x not in [np.nan] else np.nan)

    output = output.rename(columns={streetname:'Straat', town:'Plaats'})
    output = output[['Naam', 'Straat', 'Huisnummer', 'Postcode', 'Plaats']]
    output = output.drop_duplicates(subset='Naam')

    return output


def convert_to_cocon_template(dataset, streetname, housenumber, suffix, postcode, town):
    """ this function converts a dtaframe into a template that can be used for the ccc tool """

    # make a copy of the dataset to keep is
    output_w_sx = dataset.copy()
    output_wo_sx = dataset.copy()    

    # create dataframe that includes suffix
    output_w_sx['Naam'] = output_w_sx[postcode].fillna('').astype(str) + ' ' + output_w_sx[housenumber].fillna('').astype(str) + ' ' + output_w_sx[suffix].fillna('').astype(str)     
    output_w_sx['Naam'] = output_w_sx['Naam'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output_w_sx['Huisnummer'] = output_w_sx[housenumber].fillna('').astype(str) + ' ' + output_w_sx[suffix].fillna('').astype(str)
    output_w_sx['Huisnummer'] = output_w_sx['Huisnummer'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output_w_sx['Postcode'] = output_w_sx[postcode].apply(lambda x: ''.join(x.split(' ')) if x not in [np.nan] else np.nan)
    output_w_sx['inc_sx'] = True
    output_w_sx = output_w_sx.rename(columns={streetname:'Straat', town:'Plaats'})
    output_w_sx = output_w_sx[['Naam', 'Straat', 'Huisnummer', 'Postcode', 'Plaats', 'inc_sx']]

    # also add records for addresses without suffix due to large number of errors
    output_wo_sx['Naam'] = output_wo_sx[postcode].fillna('').astype(str) + ' ' + output_wo_sx[housenumber].fillna('').astype(str) + ' ' + output_wo_sx[suffix].fillna('').astype(str)     
    output_wo_sx['Naam'] = output_wo_sx['Naam'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output_wo_sx['Huisnummer'] = output_wo_sx[housenumber].fillna('').astype(str) 
    output_wo_sx['Huisnummer'] = output_wo_sx['Huisnummer'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))
    output_wo_sx['Postcode'] = output_wo_sx[postcode].apply(lambda x: ''.join(x.split(' ')) if x not in [np.nan] else np.nan)   
    output_wo_sx['inc_sx'] = False         
    output_wo_sx = output_wo_sx.rename(columns={streetname:'Straat', town:'Plaats'})
    output_wo_sx = output_wo_sx[['Naam', 'Straat', 'Huisnummer', 'Postcode', 'Plaats', 'inc_sx']]
      
    # concat and deduplicate
    final_output = pd.concat([output_w_sx, output_wo_sx])
    final_output = final_output.drop_duplicates(subset=['Naam', 'Straat', 'Huisnummer', 'Postcode', 'Plaats'])  

    return final_output


def merge_ccc(dnb, ccc):
    """ this function merges the ccc information to the dnb dataset """
    
    # create ccc_id dnb
    dnb['ID_CCC'] = dnb['Postal Code'].fillna('').astype(str) + ' ' + dnb['House number'].fillna('').astype(str) + ' ' + dnb['House number suffix'].fillna('').astype(str)    
    dnb['ID_CCC'] = dnb['ID_CCC'].apply(lambda x: x.replace(' ', '').replace('nan', '').replace('.0', ''))         

    # sort ccc and keep relevant
    ccc = ccc.sort_values(['Naam', 'Totale_kosten', 'inc_sx'], ascending=[True, True, False]).drop_duplicates(subset='Naam', keep='first')
    
    # merge info
    output = dnb.merge(ccc[['Naam', 'Netwerkafstand', 'graafafstand', 'Totale_kosten', 'Blocked_Area', 'Foutmelding', 'inc_sx']].rename(columns={'Naam':'ID_CCC'}), how='left', on='ID_CCC')

    return output
