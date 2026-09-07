"""
Fertilizer Marketplace catalog — Pakistani fertilizer companies and their
publicly known product lines/categories.

HONESTY NOTE: Company names and product line names below are real and
sourced from public company literature. Per-unit selling PRICES are
intentionally NOT included here, because no live/verified pricing feed for
these specific branded products exists yet in this build. The marketplace
shows "Contact dealer" instead of a fabricated number. Once a real vendor
price-list API or dealer network integration is connected, wire it into
`price` and `meta` on ProductListing the same way mandi/fertilizer price
services do.
"""
from pydantic import BaseModel
from typing import Optional


class FertilizerCompany(BaseModel):
    id: str
    name: str
    logo_initial: str
    description: str
    website: Optional[str] = None
    categories: list[str]


class FertilizerProduct(BaseModel):
    id: str
    company_id: str
    name: str
    category: str  # Nitrogenous / Phosphatic / Potassic / Micronutrient & Bio / NPK Blend
    nutrient_content: Optional[str] = None
    description: str
    price: Optional[float] = None  # intentionally None — see honesty note above
    unit: Optional[str] = "50kg bag"


COMPANIES: list[FertilizerCompany] = [
    FertilizerCompany(
        id="ffc",
        name="Fauji Fertilizer Company (FFC)",
        logo_initial="FFC",
        description="Pakistan's largest urea producer, known for Sona Urea, Sona DAP, and Zarkhez NPK blends.",
        website="https://www.ffc.com.pk",
        categories=["Nitrogenous", "Phosphatic", "NPK Blend"],
    ),
    FertilizerCompany(
        id="engro",
        name="Engro Fertilizers Ltd.",
        logo_initial="EF",
        description="Major producer of urea, customized NPK blends, and micronutrient fertilizers for wheat, rice, cotton and maize.",
        website="https://www.engrofertilizers.com",
        categories=["Nitrogenous", "NPK Blend", "Micronutrient & Bio"],
    ),
    FertilizerCompany(
        id="fatima",
        name="Fatima Fertilizer Company",
        logo_initial="FF",
        description="Part of the Fatima Group, producing Nitrophos, Calcium Ammonium Nitrate (CAN), and biofertilizers.",
        website="https://www.fatima-group.com/fertilizer",
        categories=["Nitrogenous", "Phosphatic", "Micronutrient & Bio"],
    ),
    FertilizerCompany(
        id="pak-arab",
        name="Pak Arab Fertilizers (Fatima Group)",
        logo_initial="PAF",
        description="Offers PakCAN, PakAS (Ammonium Sulfate), and PakZinc soil-enriching formulations.",
        website=None,
        categories=["Nitrogenous", "Micronutrient & Bio"],
    ),
    FertilizerCompany(
        id="sitara",
        name="Sitara Chemical Industries",
        logo_initial="SC",
        description="Produces Sitara Zinc, NPK blends, and organic bio-boost fertilizers for micronutrient uptake and soil health.",
        website=None,
        categories=["Micronutrient & Bio", "NPK Blend"],
    ),
    FertilizerCompany(
        id="ffbl",
        name="Fauji Fertilizer Bin Qasim Ltd. (FFBL)",
        logo_initial="FBL",
        description="Key player in DAP production, ensuring nationwide availability alongside sister company FFC.",
        website=None,
        categories=["Phosphatic"],
    ),
    FertilizerCompany(
        id="pak-agro",
        name="Pak Agro Fertilizers & Chemicals",
        logo_initial="PA",
        description="Importer, formulator and distributor offering Kisaan Sultan DAP, Ammonium Sulfate, and TSP.",
        website="https://pakagrofertilizers.com",
        categories=["Phosphatic", "Nitrogenous"],
    ),
    FertilizerCompany(
        id="suraj",
        name="Suraj Fertilizer Industries (Pvt) Ltd",
        logo_initial="SF",
        description="Specializes in Single Super Phosphate (SSP) and Sulphuric Acid, with a modern facility in Sahiwal.",
        website="https://www.surajfertilizer.com",
        categories=["Phosphatic"],
    ),
    FertilizerCompany(
        id="van",
        name="Vital Agri Nutrients (VAN)",
        logo_initial="VAN",
        description="Focuses on water-soluble fertilizers including Sulfur Coated Urea for prolonged nutrient supply.",
        website=None,
        categories=["Nitrogenous", "Micronutrient & Bio"],
    ),
    FertilizerCompany(
        id="innovative",
        name="Innovative Chemicals",
        logo_initial="IC",
        description="Produces eco-friendly organic fertilizers for commercial and home gardening applications.",
        website=None,
        categories=["Micronutrient & Bio"],
    ),
    FertilizerCompany(
        id="fdp",
        name="Farm Dynamics Pakistan (FDP)",
        logo_initial="FDP",
        description="Supplies seeds, machinery, and fertilizers supporting modern farming practices.",
        website=None,
        categories=["NPK Blend"],
    ),
]

PRODUCTS: list[FertilizerProduct] = [
    FertilizerProduct(id="ffc-sona-urea", company_id="ffc", name="Sona Urea", category="Nitrogenous",
                       nutrient_content="46% Nitrogen", description="Fast nitrogen release, Pakistan's most widely used urea brand."),
    FertilizerProduct(id="ffc-sona-dap", company_id="ffc", name="Sona DAP", category="Phosphatic",
                       nutrient_content="18-46-0", description="Slow-release phosphorus for strong root development."),
    FertilizerProduct(id="ffc-zarkhez", company_id="ffc", name="Zarkhez NPK", category="NPK Blend",
                       nutrient_content="Varies by blend", description="Balanced NPK blend formulated for major Pakistani crops."),

    FertilizerProduct(id="engro-urea", company_id="engro", name="Engro Urea", category="Nitrogenous",
                       nutrient_content="46% Nitrogen", description="Standard granular urea for nitrogen-demanding crops."),
    FertilizerProduct(id="engro-npk", company_id="engro", name="Engro Zarkhez / NPK Blends", category="NPK Blend",
                       description="Customized nutrient blends for wheat, rice, cotton and maize."),
    FertilizerProduct(id="engro-zabardast", company_id="engro", name="Engro Zabardast (micronutrient)", category="Micronutrient & Bio",
                       description="Micronutrient supplement for balanced crop nutrition."),

    FertilizerProduct(id="fatima-nitrophos", company_id="fatima", name="Nitrophos", category="Phosphatic",
                       description="Nitrogen-phosphorus compound fertilizer for sustained nutrient release."),
    FertilizerProduct(id="fatima-can", company_id="fatima", name="Calcium Ammonium Nitrate (CAN)", category="Nitrogenous",
                       nutrient_content="26% Nitrogen", description="Slow, sustained nitrogen release, well suited to arid regions."),
    FertilizerProduct(id="fatima-bio", company_id="fatima", name="Fatima Biofertilizer", category="Micronutrient & Bio",
                       description="Biological nutrient supplement to improve soil microbial activity."),

    FertilizerProduct(id="pakarab-pakcan", company_id="pak-arab", name="PakCAN", category="Nitrogenous",
                       description="Calcium Ammonium Nitrate variant with reduced nutrient leaching."),
    FertilizerProduct(id="pakarab-pakas", company_id="pak-arab", name="PakAS (Ammonium Sulfate)", category="Nitrogenous",
                       description="Ammonium sulfate fertilizer providing both nitrogen and sulfur."),
    FertilizerProduct(id="pakarab-pakzinc", company_id="pak-arab", name="PakZinc", category="Micronutrient & Bio",
                       description="Zinc micronutrient formulation to correct zinc-deficient soils."),

    FertilizerProduct(id="sitara-zinc", company_id="sitara", name="Sitara Zinc", category="Micronutrient & Bio",
                       description="Zinc sulfate product for correcting micronutrient deficiency."),
    FertilizerProduct(id="sitara-npk", company_id="sitara", name="Sitara NPK Blend", category="NPK Blend",
                       description="Balanced blend fertilizer for general crop use."),
    FertilizerProduct(id="sitara-bioboost", company_id="sitara", name="Bio-Boost Organic Fertilizer", category="Micronutrient & Bio",
                       description="Organic fertilizer to enhance soil health and nutrient uptake."),

    FertilizerProduct(id="ffbl-dap", company_id="ffbl", name="FFBL DAP", category="Phosphatic",
                       nutrient_content="18-46-0", description="Diammonium phosphate for phosphorus-demanding crops at planting."),

    FertilizerProduct(id="pakagro-kisaan-dap", company_id="pak-agro", name="Kisaan Sultan DAP", category="Phosphatic",
                       description="DAP formulation distributed under the Kisaan Sultan brand."),
    FertilizerProduct(id="pakagro-as", company_id="pak-agro", name="Ammonium Sulfate", category="Nitrogenous",
                       description="Nitrogen and sulfur source, useful on sulfur-deficient soils."),
    FertilizerProduct(id="pakagro-tsp", company_id="pak-agro", name="Triple Super Phosphate (TSP)", category="Phosphatic",
                       description="Concentrated phosphate fertilizer for high-phosphorus-demand crops."),

    FertilizerProduct(id="suraj-ssp", company_id="suraj", name="Single Super Phosphate (SSP)", category="Phosphatic",
                       description="Phosphate fertilizer that also supplies calcium and sulfur."),

    FertilizerProduct(id="van-scu", company_id="van", name="Sulfur Coated Urea", category="Nitrogenous",
                       description="Coated urea designed for prolonged, controlled nitrogen release."),

    FertilizerProduct(id="innovative-organic", company_id="innovative", name="Organic Fertilizer Range", category="Micronutrient & Bio",
                       description="Eco-friendly organic fertilizers for farms and home gardens."),

    FertilizerProduct(id="fdp-npk", company_id="fdp", name="FDP NPK Blend", category="NPK Blend",
                       description="NPK blend distributed alongside FDP's seed and machinery offerings."),
]

ALL_CATEGORIES = ["Nitrogenous", "Phosphatic", "Potassic", "NPK Blend", "Micronutrient & Bio"]
