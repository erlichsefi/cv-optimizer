from utils.pdf_util import extract_3


def test_pdf_reader():
    text = extract_3("data_set/Curriculum_Vitae_Jan24.pdf")
    
    keyword_must_contain = [
        "Sefi Erlich",
        "TLV, Israel - willing to relocate",
        "github.com/erlichsefi",
        "erlichsefi@gmail.com",
        "+972 524 307 093",
        "M.Sc Computer Science",
        "Thesis: Development of a Polynomial Time Algorithm for an deterministic automated negotiation AI in avarious of scenarios",
        "B.Sc Mathematics and Computer Science",
        "Ariel University, 92.7, Twice Dean Honor, Magna Cum Laude.",
        "Negotiation Strategies for Agents with Ordinal Preferences: Theoretical Analysis and Human Study",
        #"STWSN: A Novel Secure Distributed Transport Protocol for Wireless Sensor Network",
        "Negotiation Strategies for Agents with Ordinal Preference",
        "Heterogeneous SDN controller placement problem—The Wi-Fi and 4G LTE-U case"
        ]
    for keyword in keyword_must_contain:
        if keyword not in text.replace("\n","").replace("\t",""):
            assert False,f"Keyword '{keyword}' not in text"

