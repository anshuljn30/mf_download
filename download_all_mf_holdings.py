import download_axis_holdings as axis
import download_pioneer_holdings as baroda_pioneer
import download_birla_holdings as birla_sunlife
import download_paribas_holdings as bnp_paribas
import download_boi_holdings as boi_axa
import download_canara_holdings as canara_robeco
import download_dhfl_holdings as dhfl_pramerica
import download_dsp_holdings as dsp_blackrock
import download_edelweiss_holdings as edelweiss
import download_escorts_holdings as escorts
import download_essel_holdings as essel
import download_templeton_holdings as franklin_templeton
import download_hdfc_holdings as hdfc
#import download_hsbc_holdings as hsbc
import download_icici_holdings as icici_prudential
import download_idbi_holdings as idbi
import download_idfc_holdings as idfc
#import download_iifl_holdings as iifl
import download_indiabulls_holdings as indiabulls
import download_invesco_holdings as invesco
import download_jm_holdings as jm_financial
import download_kotak_holdings as kotak
import download_lic_holdings as lic
import download_lnt_holdings as lnt
import download_mirae_holdings as mirae
import download_mahindra_holdings as mahindra
import download_motilal_holdings as motilal_oswal
import download_ppfas_holdings as ppfas
import download_principal_holdings as principal
import download_quantum_holdings as quantum
import download_reliance_holdings as reliance
import download_sahara_holdings as sahara
import download_sbi_holdings as sbi
import download_shriram_holdings as shriram
import download_srei_holdings as srei
import download_sundaram_holdings as sundaram
import download_tata_holdings as tata
import download_taurus_holdings as taurus
import download_union_holdings as union
#import download_uti_holdings as uti


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