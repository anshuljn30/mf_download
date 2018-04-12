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


def main(dates, path):
    # Files Already downloaded
    axis.download(dates, path)
    baroda_pioneer.download(dates, path)
    bnp_paribas.download(dates, path)
    boi_axa.download(dates, path)
    canara_robeco.download(dates, path)
    edelweiss.download(dates, path)
    franklin_templeton.download(dates, path)
    idbi.download(dates, path)
    idfc.download(dates, path)
    indiabulls.download(dates, path)
    mahindra.download(dates)
    mirae.download(dates, path)
    motilal_oswal.download(dates, path)
    ppfas.download(dates, path)
    principal.download(dates, path)
    reliance.download(dates, path)
    shriram.download(dates, path)
    tata.download(dates, path)
    taurus.download(dates, path)
    union.download(dates, path)

    # Files already downloaded but can't be parsed - no ISIN
    escorts.download(dates, path)

    # Files yet to be downloaded
    birla_sunlife.download(dates, path)
    dhfl_pramerica.download(dates, path)
    dsp_blackrock.download(dates, path)
    essel.download(dates, path)
    hdfc.download(dates, path)
    hsbc.download(dates, path)
    icici_prudential.download(dates, path)
    iifl.download(dates, path)
    invesco.download(dates, path)
    jm_financial.download(dates, path)
    kotak.download(dates, path)
    lic.download(dates, path)
    lnt.download(dates, path)
    quantum.download(dates, path)
    sahara.download(dates, path)
    sbi.download(dates, path)
    srei.download(dates, path)
    sundaram.download(dates, path)
    uti.download(dates, path)