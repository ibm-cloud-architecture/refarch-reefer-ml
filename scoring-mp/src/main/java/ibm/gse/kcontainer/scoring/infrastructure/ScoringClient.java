package ibm.gse.kcontainer.scoring.infrastructure;

import ibm.gse.kcontainer.scoring.domain.Telemetry;

import static javax.ws.rs.core.MediaType.APPLICATION_JSON;

import java.io.StringReader;
import java.net.URI;
import java.net.URL;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.json.JsonReader;
import javax.ws.rs.core.Response;
import javax.inject.Inject;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import org.eclipse.microprofile.config.inject.ConfigProperty;

/**
 * Call remote predictive scoring deploy on CP for data via WML.
 */
public class ScoringClient {


    private Client client;
    private String mlToken = null;
    @Inject
    @ConfigProperty(name = "cp4d_base_url", defaultValue="https://zen-cpd-zen.apps.cp4dperf5.demo.ibmcloud.com")
    private String endPointURL;
    @Inject
    @ConfigProperty(name = "cp4d_prediction_url",  defaultValue="/v4/deployments/bea7d396-88c5-41fa-a622-1a92deb2bb9e/predictions")
    private String predictionURL;
    @Inject
    @ConfigProperty(name = "cp4d_user", defaultValue="jboyer")
    private String username;
    @Inject
    @ConfigProperty(name = "cp4d_pwd", defaultValue="cp4d123")
    private String password;

    private SSLContext sslcontext;

    public ScoringClient() {
        initSSL();
    }

    public ScoringClient(String url,String username, String pwd) {
        this.endPointURL = url;
        this.username = username;
        this.password = pwd;
        initSSL();
    }

    private void initSSL() {
        try {
            sslcontext = SSLContext.getInstance("TLS");
            sslcontext.init(null, new TrustManager[]{new X509TrustManager() {
                public void checkClientTrusted(X509Certificate[] arg0, String arg1) throws CertificateException {}
                public void checkServerTrusted(X509Certificate[] arg0, String arg1) throws CertificateException {}
                public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
            }}, new java.security.SecureRandom());
            client = ClientBuilder.newBuilder().sslContext(this.sslcontext).hostnameVerifier((s1,s2) -> true)
                .build();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void close(){
        this.client.close();
    }

    public String getIAMToken() {
        String token = null;
        Response resAuth = null;
        try {
            final WebTarget targetAuth = client.target(endPointURL + "/v1/preauth/validateAuth");
            
            resAuth = targetAuth.request().header("username", username).header("password", password).get();
            System.out.println(resAuth.getStatus());
            JsonReader reader = Json.createReader(new StringReader(resAuth.readEntity(String.class)));
            JsonObject ibmAMResponse = reader.readObject();
           
            token = ibmAMResponse.getString("accessToken");
            resAuth.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (resAuth != null) {
                resAuth.close();
            }
        }
        System.out.println("Token = " + token);
        return token;
    }

	public ScoringResult callAnomalyScoring(Telemetry t) {
        if (mlToken == null) {
                synchronized (this) { 
                    mlToken = getIAMToken();
                }
        }
        
        WebTarget targetResource = client.target(endPointURL + predictionURL);
        Entity entity = null; 
        Response  rep = targetResource.request().header("Content-Type", APPLICATION_JSON)
            .header("Authorization", "Bearer " + mlToken)
            .accept(APPLICATION_JSON)
            .post(entity);
        ScoringResult result = rep.readEntity(ScoringResult.class);
       
       return result;
    }

	public void setPredictiveURL(String pURL) {
        this.predictionURL = pURL;
	}
}