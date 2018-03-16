import download_axis_data as axis
import download_pioneer_data as baroda_pioneer
import download_birla_data as birla_sunlife
import download_paribas_data as bnp_paribas
import download_boi_data as boi_axa
import download_canara_data as canara_robeco
import download_dhfl_data as dhfl_pramerica
import download_blackrock_data as dsp_blackrock
import download_edelweiss_data as edelweiss
import download_escorts_data as escorts
import download_essel_data as essel
import download_templeton_data as franklin_templeton
import download_hdfc_data as hdfc
import download_hsbc_data as hsbc
import download_icici_data as icici_prudential
import download_idbi_data as idbi
import download_idfc_data as idfc
import download_iifl_data as iifl
import download_indiabulls_data as indiabulls
import download_invesco_data as invesco
import download_jmfinancial_data as jm_financial
import download_kotak_data as kotak
import download_lic_data as lic
import download_lnt_data as lnt
import download_mirae_data as mirae
import download_mahindra_data as mahindra
import download_motilal_data as motilal_oswal
import download_ppfas_data as ppfas
import download_principal_data as principal
import download_quantum_data as quantum
import download_reliance_data as reliance
import download_sahara_data as sahara
import download_sbi_data as sbi
import download_shriram_data as shriram
import download_srei_data as srei
import download_sundaram_data as sundaram
import download_tata_data as tata
import download_taurus_data as taurus
import download_union_data as union
import download_uti_data as uti


def main(dates):
    # Files Already downloaded
    axis.download(dates)
    baroda_pioneer.download(dates)
    bnp_paribas.download(dates)
    boi_axa.download(dates)
    canara_robeco.download(dates)
    edelweiss.download(dates)
    franklin_templeton.download(dates)
    idbi.download(dates)
    idfc.download(dates)
    indiabulls.download(dates)
    mahindra.download(dates)
    mirae.download(dates)
    motilal_oswal.download(dates)
    ppfas.download(dates)
    principal.download(dates)
    reliance.download(dates)
    shriram.download(dates)
    tata.download(dates)
    taurus.download(dates)
    union.download(dates)

    # Files already downloaded but can't be parsed - no ISIN
    escorts.download(dates)

    # Files yet to be downloaded
    birla_sunlife.download(dates)
    dhfl_pramerica.download(dates)
    dsp_blackrock.download(dates)
    essel.download(dates)
    hdfc.download(dates)
    hsbc.download(dates)
    icici_prudential.download(dates)
    iifl.download(dates)
    invesco.download(dates)
    jm_financial.download(dates)
    kotak.download(dates)
    lic.download(dates)
    lnt.download(dates)
    quantum.download(dates)
    sahara.download(dates)
    sbi.download(dates)
    srei.download(dates)
    sundaram.download(dates)
    uti.download(dates)