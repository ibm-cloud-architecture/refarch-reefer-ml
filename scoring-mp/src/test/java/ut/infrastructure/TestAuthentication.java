package ut.infrastructure;

import org.junit.Test;

import java.io.StringReader;

import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;

public class TestAuthentication {

    @Test
    public void TestDeserialization() {
        String response = "{\"username\":\"jboyer\",\"role\":\"User\"," +
         "\"permissions\": [\"access_catalog\",\"access_information_assets\",\"view_quality\",\"manage_information_assets\",\"manage_metadata_import\",\"manage_discovery\",\"author_governance_artifacts\",\"manage_quality\",\"can_provision\"],"+
         "\"sub\":\"jboyer\",\"iss\":\"KNOXSSO\",\"aud\":\"DSX\",\"uid\":\"1000331016\"," + 
         "\"authenticator\":\"default\",\"accessToken\":\"eyJhbpbXBvcYblrYMA\"," +
         "\"_messageCode_\":\"success\",\"message\":\"success\"}";

         JsonReader reader = Json.createReader(new StringReader(response));
         
         JsonObject ibmAMResponse = reader.readObject();
         System.out.println("username    : " + ibmAMResponse.getString("username"));
         System.out.println("accessToken : " + ibmAMResponse.getString("accessToken"));
         System.out.println("permissions : " + ibmAMResponse.getJsonArray("permissions"));
         reader.close();

    }


}