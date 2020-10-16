<template>
  <v-app>
    <v-container
      fluid
      class="px-10">

      <!-- Верхняя строка -->
      <v-row
        align="center"
        justify="space-between"
        class="pa-0 ma-0">
        <v-col
          cols="12"
          md="7"
          class="pa-0 ma-0"
        >
          <v-card-title class="pa-0 ma-0">
            Занимаемые должности
          </v-card-title>
        </v-col>
        <v-col
          cols="12"
          md="5"
          class="pa-0 ma-0"
        >
          <v-card-title class="pa-0 ma-0">
            <v-text-field
              v-model="name"
              type="text"
              label="Поиск по сотруднику"
              append-icon="mdi-magnify"
            ></v-text-field>
          </v-card-title>
        </v-col>
      </v-row>

      <!-- Нижняя строка -->
      <v-row
        align="center"
        justify="end"
        class="pa-0 ma-0">
        <div class="checkbox">
          <v-checkbox
            v-model="checked"
            label="Показать уволенных"
            color="success"
            class="mr-5 mb-10"
          ></v-checkbox>
        </div>
        <v-btn
          normal
          color="green lighten-3"
          class="mr-5 mb-10"
        >Принять на должность</v-btn>
        <v-btn
          normal
          color="green lighten-3"
          class="mb-10"
          :disabled="selectedRows.length === 0"
          @click="toFire()"
        >
          <span v-if="selectedRows.length <= 1">Снять с должности</span>
          <span v-if="selectedRows.length > 1">Снять с должностей</span>
        </v-btn>
      </v-row>

      <!-- Таблица -->
      <v-data-table
        :headers="headers"
        :items="occupations"
        item-key="name"
      >
        <template v-slot:item="props">
          <tr
            :class="{'grey lighten-2' : selectedRows.includes(props.item) &&
                                        props.item.fireDate === null,
                     'red lighten-2 disabled' : props.item.fireDate !== null}"
            @click="props.item.fireDate === null ? rowClicked(props.item) : false"
            v-if="checked || props.item.fireDate === null"
          >
            <td>{{ props.item.name }}</td>
            <td>{{ props.item.companyName }}</td>
            <td>{{ props.item.positionName }}</td>
            <td>{{ props.item.hireDate.replace(/(\d+)-(\d+)-(\d+)/, '$3.$2.$1') }}</td>
            <td>{{ typeof props.item.fireDate === 'string' ?
                          props.item.fireDate.replace(/(\d+)-(\d+)-(\d+)/, '$3.$2.$1') :
                          props.item.fireDate }}
            </td>
            <td>
              <v-edit-dialog
                :return-value.sync="props.item.salary"
                v-model="props.item.fraction"
                large
                persistent
                cancel-text="Отменить"
                save-text="Сохранить"
              >
                <div>{{ props.item.salary }} ₽ ({{ props.item.fraction }})%</div>
                <template v-slot:input>
                  <v-row>
                    <v-col
                      cols="12"
                      md="6"
                      style="width: 100px"
                    >
                      <div class="mt-3">Ставка, ₽</div>
                      <v-text-field
                        type="number"
                        v-model="props.item.salary"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      md="6"
                    >
                      <div class="mt-3">Ставка, %</div>
                      <v-text-field
                        type="number"
                        v-model="props.item.fraction"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </template>
              </v-edit-dialog>
            </td>
            <td>
              <v-edit-dialog
                :return-value.sync="props.item.base"
                large
                persistent
                cancel-text="Отменить"
                save-text="Сохранить"
              >
                <div>{{ props.item.base }}</div>
                <template v-slot:input>
                  <div class="mt-3">База, ₽</div>
                  <v-text-field
                    type="number"
                    v-model="props.item.base"
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>
            <td>
              <v-edit-dialog
                :return-value.sync="props.item.advance"
                large
                persistent
                cancel-text="Отменить"
                save-text="Сохранить"
              >
                <div>{{ props.item.advance }}</div>
                <template v-slot:input>
                  <div class="mt-3">Аванс, ₽</div>
                  <v-text-field
                    type="number"
                    v-model="props.item.advance"
                  ></v-text-field>
                </template>
              </v-edit-dialog>
            </td>
            <td>
              <v-simple-checkbox
                v-model="props.item.byHours"
                color="success"
              ></v-simple-checkbox>
            </td>
          </tr>
        </template>
      </v-data-table>
      <div>Массив с выделенными строками: <br>
        {{ selectedRows }}
      </div>
      <div>Данные полученные с сервера: <br>
        {{ occupations }}
      </div>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios'
export default {
  name: 'vTable',
  components: {},
  data: () => ({
    search: '',
    name: '',
    checked: false,
    selectedRows: [],
    disable: true,
    occupations: []
  }),
  methods: {
    toFire() {
      this.selectedRows.map((item, index, array) => {
        item.fireDate = new Date();

        var day = String(item.fireDate.getDate()).padStart(2, '0');
        var month = String(item.fireDate.getMonth() + 1).padStart(2, '0');
        var year = item.fireDate.getFullYear();

        item.fireDate = day + '.' + month + '.' + year;
      })
      this.selectedRows.length = 0
    },
    rowClicked(row) {
      this.toggleSelection(row);
    },
    toggleSelection(key) {
      if (this.selectedRows.includes(key)) {
        this.selectedRows = this.selectedRows.filter(
          selectedKey => selectedKey !== key
        )
      } else {
        this.selectedRows.push(key);
      }
    },
  },
  computed: {
    headers() {
      return [
        {
          text: 'Сотрудник',
          value: 'name',
          filter: f => { return ( f + '' ).toLowerCase()
                                          .includes( this[ 'name' ]
                                          .toLowerCase())}
        },
        { text: 'Компания', value: 'companyName' },
        { text: 'Должность', value: 'positionName' },
        { text: 'Дата приема', value: 'hireDate' },
        { text: 'Дата увольнения', value: 'fireDate' },
        { text: 'Ставка', value: 'salary' },
        { text: 'База', value: 'base' },
        { text: 'Аванс', value: 'advance' },
        { text: 'Почасовая', value: 'byHours' },
      ]
    },
  },
  async mounted () {
    	try {
    		var result = await axios({
    			method: 'POST',
    			url: 'http://127.0.0.2:8000/graphql/',
    			data: {
    				query: `
    				{
					  occupations {
              id
              name
              companyName
              positionName
              hireDate
              fireDate
              salary
              fraction
              base
              advance
              byHours
            }
					}
    				`
    			}
    		})
    		this.occupations = result.data.data.occupations
    	} catch (error) {
    		console.error(error)
    	}
    }
};
</script>

<style>
.disabled {
  pointer-events: none;
}
</style>